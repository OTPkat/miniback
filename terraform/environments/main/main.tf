provider "google" {
  project = var.project
  region = var.location
}

data "google_client_config" "default" {}

provider "docker" {
  registry_auth {
    address = "gcr.io"
    username = "oauth2accesstoken"
    password = data.google_client_config.default.access_token
  }
}

data "docker_registry_image" "fastgames_worker_image" {
  name = "gcr.io/${var.project}/${var.docker_image_name}"
}

data "google_container_registry_image" "fastgames_latest" {
  name = var.docker_image_name
  project = var.project
  digest = data.docker_registry_image.fastgames_worker_image.sha256_digest
}


resource "google_sql_database_instance" "instance" {
  name             = var.sql_instance_name
  project          = var.project
  database_version = var.db_version
  region = var.location
  settings {
    tier = var.tier
    availability_type = "REGIONAL"
    disk_autoresize = true
    backup_configuration {
      enabled = true
    }
  }
}

resource "google_sql_database" "fastgames_db" {
  instance = google_sql_database_instance.instance.name
  name = var.db_name
}

resource "random_password" "fastgames_user_password" {
  length = 16
}

resource "google_sql_user" "fastgames_user" {
  instance = google_sql_database_instance.instance.name
  name = "fastgames"
  password = random_password.fastgames_user_password.result
}

resource "google_project_service" "secretmanager" {
  service  = "secretmanager.googleapis.com"
}


resource "google_secret_manager_secret" "fastgames-db-secret" {
  provider = google-beta
  project = var.project
  secret_id = "fastgames-db"

  replication {
    automatic = true
  }

  depends_on = [google_project_service.secretmanager]
}

resource "google_secret_manager_secret_version" "fastgames-db-secret-1" {
  secret      = google_secret_manager_secret.fastgames-db-secret.id
  secret_data = google_sql_user.fastgames_user.password
}


module "worker" {
  source = "../../modules/cloudrunworker"
  docker_image = data.google_container_registry_image.fastgames_latest.image_url
  location = var.location
  worker_name = var.worker_name
  project = var.project
  db_user_name = google_sql_user.fastgames_user.name
  db_user_password_secret_id = google_secret_manager_secret_version.fastgames-db-secret-1.id
  db_name = var.db_name
  sql_instance_connection_name = google_sql_database_instance.instance.connection_name
  service_account_name = google_service_account.fastgames_gsa.email
}


# Creates a service account for the cloud worker
resource "google_service_account" "fastgames_gsa" {
  account_id = "fastgames-service"
  display_name = "The service for cloud run for the back end!"
}

resource "google_project_iam_member" "fastgames_iam" {
  for_each = toset([
    "roles/run.developer",
    "roles/cloudsql.editor",
    "roles/secretmanager.secretAccessor",
    "roles/storage.objectCreator"])
  project = var.project
  role = each.key
  member = "serviceAccount:${google_service_account.fastgames_gsa.email}"
}
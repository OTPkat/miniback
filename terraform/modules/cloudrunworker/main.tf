resource "google_cloud_run_service" "fastgames_worker" {
  name     = var.worker_name
  location = var.location
  project = var.project

  template {
    spec {
      service_account_name = var.service_account_name

      containers {
        image = var.docker_image

        env {
          name  = "POSTGRES_DB"
          value = var.db_name
        }

        env {
          name  = "POSTGRES_USER"
          value = var.db_user_name
        }

        env {
          name  = "POSTGRES_PASSWORD_SECRET_ID"
          value = var.db_user_password_secret_id
        }

        env {
          name = "CLOUD_SQL_CONNECTION_NAME"
          value = var.sql_instance_connection_name
        }
      }

    }
    metadata {
      annotations = {
        "autoscaling.knative.dev/maxScale"      = "1000"
        "run.googleapis.com/cloudsql-instances" = var.sql_instance_connection_name
        "run.googleapis.com/client-name"        = "terraform"
      }
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}
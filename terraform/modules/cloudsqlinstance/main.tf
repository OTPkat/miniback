resource "google_sql_database_instance" "archive_mint_sql_instance" {
  name             = var.instance_name
  database_version = var.database_version
  region = var.region
  deletion_protection = var.delete_protection
  settings {
    tier = var.tier
    availability_type = "REGIONAL"
    disk_autoresize = true
    backup_configuration {
      enabled = true
    }
  }
}
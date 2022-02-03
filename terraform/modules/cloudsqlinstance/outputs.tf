output "db_master_name" {
  value = google_sql_database_instance.archive_mint_sql_instance.name
}

output "connection_name" {
  value = google_sql_database_instance.archive_mint_sql_instance.connection_name
}
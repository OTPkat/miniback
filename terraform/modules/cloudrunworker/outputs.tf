output "backend_address" {
  value = google_cloud_run_service.fastgames_worker.status[0].url
}

output "service" {
  value = google_cloud_run_service.fastgames_worker.name
}

output "project" {
  value = google_cloud_run_service.fastgames_worker.project
}

output "location" {
  value = google_cloud_run_service.fastgames_worker.location
}
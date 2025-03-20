output "bucket_name" {
  description = "The name of the created GCS bucket"
  value       = google_storage_bucket.data_bucket.name
}

output "bucket_url" {
  description = "The URL of the created GCS bucket"
  value       = google_storage_bucket.data_bucket.url
}

output "bigquery_dataset_id" {
  description = "The ID of the created BigQuery dataset"
  value       = google_bigquery_dataset.default.dataset_id
}

output "service_account_email" {
  description = "The email address of the created service account"
  value       = google_service_account.daredata.email
}

output "service_account_id" {
  description = "The ID of the created service account"
  value       = google_service_account.daredata.id
} 
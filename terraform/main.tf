# Enable required APIs
resource "google_project_service" "storage_api" {
  service            = "storage-api.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "bigquery_api" {
  service            = "bigquery.googleapis.com"
  disable_on_destroy = false
}

resource "google_project_service" "iam_api" {
  service            = "iam.googleapis.com"
  disable_on_destroy = false
}

# Create GCS bucket
resource "google_storage_bucket" "data_bucket" {
  name     = var.bucket_name
  location = var.region
  force_destroy = true
  
  depends_on = [google_project_service.storage_api]
}

# Create BigQuery dataset
resource "google_bigquery_dataset" "default" {
  dataset_id                  = var.dataset_id
  friendly_name               = "Daredata Challenge Dataset"
  description                 = "Dataset for the Daredata challenge"
  location                    = var.region
  
  depends_on = [google_project_service.bigquery_api]
}

# Create Service Account
resource "google_service_account" "daredata" {
  account_id   = var.service_account_name
  display_name = "Daredata Service Account"
  
  depends_on = [google_project_service.iam_api]
}

# Assign BigQuery Admin role to service account
resource "google_project_iam_binding" "bigquery_admin" {
  project = var.project_id
  role    = "roles/bigquery.admin"
  
  members = [
    "serviceAccount:${google_service_account.daredata.email}"
  ]
}

# Grant storage object viewer role for reading from buckets
resource "google_project_iam_binding" "storage_object_viewer" {
  project = var.project_id
  role    = "roles/storage.objectViewer"
  
  members = [
    "serviceAccount:${google_service_account.daredata.email}"
  ]
} 
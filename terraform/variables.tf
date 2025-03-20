variable "project_id" {
  description = "The GCP project ID"
  type        = string
}

variable "region" {
  description = "The GCP region for resources"
  type        = string
  default     = "europe-west1"
}

variable "bucket_name" {
  description = "Name for the GCS bucket"
  type        = string
  default     = "daredata-storage"
}

variable "dataset_id" {
  description = "ID for the BigQuery dataset"
  type        = string
  default     = "daredata_dataset"
}

variable "service_account_name" {
  description = "Name of the service account to create"
  type        = string
  default     = "daredata"
} 
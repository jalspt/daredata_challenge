terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
  }
  required_version = ">= 1.0.0"
}

provider "google" {
  # Project ID to be specified via environment variable or tfvars
  project = var.project_id
  region  = var.region
} 
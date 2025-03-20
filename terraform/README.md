# Terraform Configuration for GCP Resources

This Terraform configuration sets up the following GCP resources:

- GCS Bucket for data storage
- BigQuery Dataset for data analysis
- Service Account "daredata" with BigQuery Admin and Storage Object Viewer permissions
- Enables necessary GCP APIs

## Prerequisites

- Terraform installed locally (v1.0.0 or newer)
- GCP account with a project
- gcloud CLI configured with appropriate permissions

## Usage

1. Copy `terraform.tfvars.example` to `terraform.tfvars` and update with your GCP project ID:

```bash
cp terraform.tfvars.example terraform.tfvars
```

2. Edit `terraform.tfvars` with your specific values

3. Initialize Terraform:

```bash
terraform init
```

4. Check the execution plan:

```bash
terraform plan
```

5. Apply the changes:

```bash
terraform apply
```

6. To destroy the resources:

```bash
terraform destroy
```

## Resources Created

- GCS bucket for data storage
- BigQuery dataset
- Service account with BigQuery Admin permissions
- Necessary API enablements

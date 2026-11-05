variable "bucket_name" {
    description = "Globally uniq name for the S3 OICARC compliance archive bucket"
    type = string
}

variable "retention_years" {
    description = "Statutory SOX Section 404 data retention schedule in years"
    type = number
    default = 4
}

variable "environment" {
  description = "Deployment environment (production, staging, lab)"
  type = string
  default = "production"
}
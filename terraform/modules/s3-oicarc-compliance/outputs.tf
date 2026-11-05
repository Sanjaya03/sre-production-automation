output "bucket_id" {
 description = "The name of the OICARC compliance bucket" 
 value = aws_s3_bucket.oicarc_archive.id
}

output "bucket_arn" {
  description = "The ARN of the OICARC compliance bucket"
  value = aws_s3_bucket.oicarc_archive.arn
}

output "kms_key_arn" {
  description = "The ARN of the KMS Customer Managed Key encrypting the archive"
  value = aws_kms_key.oicarc_key.arn
}

output "retention_mode" {
  description = "Active Object Lock retention mode"
  value = "COMPLIANCE"
}

output "retention_years" {
  description = "Statutory retention duration in years"
  value = var.retention_years
}
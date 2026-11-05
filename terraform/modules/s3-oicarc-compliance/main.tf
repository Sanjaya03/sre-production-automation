resource "aws_kms_key" "oicarc_key" {
    description = "KMS CMK for OICARC financial archive encryption at rest"
    deletion_window_in_days = 30
    enable_key_rotation = true
    tags = {
      Platform = "Enterprise-Sales-Compensation"
      Subsystem = "OICARC"
      DataClassification = "SOX-Financial-Confidential"
      Environment = var.environment
      ManagedBy = "Terraform"
    }
}

resource "aws_kms_alias" "oicarc_key_alias" {
    name = "alias/enterprise-salescomp-oicarc-${var.environment}"
    target_key_id = aws_kms_key.oicarc_key.key_id
}

resource "aws_s3_bucket" "oicarc_archive" {
    bucket = var.bucket_name
    force_destroy = false
    object_lock_enabled = true
    tags = {
      Platform = "Enterprise-Sales-Compensation"
      Subsystem = "OICARC"
      DataClassification = "SOX-Financial-Confidential"
      Environment = var.environment
      ManagedBy = "Terraform"
    }
}

resource "aws_s3_bucket_versioning" "oicarc_versioning" {
    bucket = aws_s3_bucket.oicarc_archive.id
    versioning_configuration {
      status = "Enabled"
    }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "oicarc_encryption" {
    bucket = aws_s3_bucket.oicarc_archive.id
    rule {
        apply_server_side_encryption_by_default {
          kms_master_key_id = aws_kms_key.oicarc_key.arn
          sse_algorithm = "aws:kms"
        }
        bucket_key_enabled = true
    }
}

resource "aws_s3_bucket_public_access_block" "oicarc_public_block" {
  bucket = aws_s3_bucket.oicarc_archive.id
  
  block_public_acls = true
  block_public_policy = true
  ignore_public_acls = true
  restrict_public_buckets = true
}

resource "aws_s3_bucket_object_lock_configuration" "oicarc_lock" {
  bucket = aws_s3_bucket.oicarc_archive.id
  rule {
    default_retention {
      years = var.retention_years
      mode = "COMPLIANCE"
    }
  }
  depends_on = [aws_s3_bucket_versioning.oicarc_versioning]
}

resource "aws_s3_bucket_policy" "oicarc_policy" {
  bucket = aws_s3_bucket.oicarc_archive.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Sid = "EnforceTLSRequestsOnly"
      Effect = "Deny"
      Principal = "*"
      Action = "s3:*"
      Resource = [
        aws_s3_bucket.oicarc_archive.arn,
        "${aws_s3_bucket.oicarc_archive.arn}/*"
      ]
      Condition = {
        Bool = {
          "aws:SecureTransport" = "false"
        }
      }
    }]
  })
}

resource "aws_s3_bucket_lifecycle_configuration" "oicarc_lifecycle" {
  bucket = aws_s3_bucket.oicarc_archive.id

  rule {
    id = "archive-cold-sox-records"
    status = "Enabled"
    filter {}
    transition {
      days = 365
      storage_class = "GLACIER"
    }
  }
  depends_on = [aws_s3_bucket_versioning.oicarc_versioning]
}

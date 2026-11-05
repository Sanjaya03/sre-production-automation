terraform {
  required_version = ">= 1.5.0"
  required_providers {
    aws = {
        source = "hashicorp/aws"
        version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

module "s3_oicarc_compliance_archive" {
    source = "../../modules/s3-oicarc-compliance"
    bucket_name = "enterprise-salescomp-oicarc-archive-316704942171"
    retention_years = 4
    environment = "production"
}

output "oicarc_bucket_arn" {
  description = "ARN for OICARC audit compliance bucket"
  value = module.s3_oicarc_compliance_archive.bucket_arn
}

output "oicarc_kms_key_arn" {
  description = "ARN for OICARC KMS Customer Managed Key"
  value = module.s3_oicarc_compliance_archive.kms_key_arn
}
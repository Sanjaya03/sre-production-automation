# Enterprise Cloud Infrastructure & Compliance Automation (AWS & Terraform)

## Platform Overview
Production Infrastructure as Code (IaC) repository provisioning cloud foundations for an enterprise Sales & Incentive Compensation Platform ($2B+ in annual commission payouts across 15,000+ sales personnel under strict SOX ITGC Section 404 compliance).

Architecture Flow:
[15,000 Sales Representatives / Upstream Order Feeds]
         │
         ▼
[AWS 3-Tier Multi-AZ VPC: 10.100.0.0/16]
   ├── Public Subnets (ALB / Ingress Gateway)
   ├── Private Compute Subnets (EKS Calculation Engine - QIC)
   └── Private Database Subnets (PostgreSQL 16 & PgBouncer)
         │
         ▼ (Settled Commission Payout Archive)
[OICARC Statutory Archival Tier: AWS S3 & KMS CMK]
   ├── WORM Object Lock in COMPLIANCE Mode (4-Year Legal Hold)
   ├── SSE-KMS Encryption with Annual Key Rotation & Bucket Key
   ├── In-Transit TLS Enforcement (Deny non-HTTPS)
   └── FinOps Lifecycle Transition to S3 Glacier after 1 Year

---

## Modular Architecture

terraform/
├── modules/
│   └── s3-oicarc-compliance/      # Statutory WORM archive module
│       ├── main.tf                # S3 Bucket, KMS Key, WORM Lock, TLS Policy, Glacier Lifecycle
│       ├── variables.tf           # Input schema & parameterization
│       └── outputs.tf             # Public module interface (Bucket & KMS ARNs)
└── environments/
    └── prod/                      # Production root deployment
        └── main.tf                # Environment-specific parameterization & output exports

---

## SOX ITGC Security Controls Implemented

| Security Control | Implementation Primitive | Purpose |
| :--- | :--- | :--- |
| Data Immutability (WORM) | aws_s3_bucket_object_lock_configuration | Enforces non-bypassable COMPLIANCE mode for 4 years; prevents deletion or alteration by any identity, including root. |
| Dual-Layer Authorization | aws_kms_key & aws_kms_alias | Customer Managed Key (CMK) enforcing Segregation of Duties (SoD); requires both s3:GetObject and kms:Decrypt. |
| Cryptographic Rotation | enable_key_rotation = true | Automatic annual key rotation satisfying NIST SP 800-57 guidelines. |
| FinOps Cost Optimization | bucket_key_enabled = true | Caches bucket-level keys in S3, reducing KMS API request charges by up to 99%. |
| Data in Transit | aws_s3_bucket_policy | Explicit Deny statement rejecting any connection where aws:SecureTransport == false. |
| Long-Term Retention | aws_s3_bucket_lifecycle_configuration | Automatically transitions settled archives to Glacier Flexible Retrieval after 365 days (80% cost reduction). |

---

## Verification & Validation Commands
- terraform init
- terraform validate
- terraform plan

## Author
Sanjaya Kumar Swain — Senior Site Reliability Engineer / Database Reliability Engineer (DBRE)
Public Codebases: github.com/Sanjaya03

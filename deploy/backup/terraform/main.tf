terraform {
  backend "s3" {
    bucket  = "fluidattacks-terraform-states-prod"
    key     = "integrates-prod-backup.tfstate"
    region  = "us-east-1"
    encrypt = true
  }
}

provider "aws" {
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
  version    = ">= 2.11"
  region     = var.region
}

resource "aws_backup_vault" "backup_vault" {
  name        = "integrates-backup-vault"
  kms_key_arn = "arn:aws:kms:us-east-1:205810638802:key/d33073aa-19f8-4390-afa1-abcda2be27d7"
}

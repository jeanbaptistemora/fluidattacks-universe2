variable "vaultBucket" {}

data "aws_caller_identity" "current_account" {}

data "aws_iam_policy_document" "key_access_policy" {
  statement {
    sid     = "Allow Access to EKSNode role"
    actions = ["kms:Encrypt", "kms:Decrypt"]
    resources = ["*"]

    principals {
      type        = "AWS"
      identifiers = [aws_iam_role.k8s_nodes_role.arn]
    }
  }

  statement {
    sid     = "Allow key management to Master acccount"
    actions = [
      "kms:Create*",
      "kms:Describe*",
      "kms:Enable*",
      "kms:List*",
      "kms:Put*",
      "kms:Update*",
      "kms:Revoke*",
      "kms:Disable*",
      "kms:Get*",
      "kms:Delete*",
      "kms:ScheduleKeyDeletion",
      "kms:CancelKeyDeletion",
      "kms:TagResource",
      "kms:UntagResource",
      "kms:ListResourceTags"
    ]
    resources = ["*"]

    principals {
      type        = "AWS"
      identifiers = [data.aws_caller_identity.current_account.arn]
    }
  }
}

resource "aws_kms_key" "vault_encryption_key" {
  description             = "Key used to encrypt and store Vault unseal key"
  deletion_window_in_days = 30
  policy = data.aws_iam_policy_document.key_access_policy.json

  tags = {
    Name = "Encryption_Key_Vault"
    App  = "Vault"
  }
}

resource "aws_kms_alias" "vault_key_alias" {
  name          = "alias/vault-key"
  target_key_id = aws_kms_key.vault_encryption_key.key_id
}

resource "aws_s3_bucket" "vault" {
  bucket = var.vaultBucket
  acl    = "private"

  lifecycle_rule {
    id      = "cleanup"
    prefix  = "vault.etcd"
    enabled = true
    expiration {
      days  = 30
    }
  }

  tags = {
    Name = "Vault_Bucket"
    App  = "Vault"
  }
}

output "vaultKmsKey" {
  value     = aws_kms_key.vault_encryption_key.key_id
  sensitive = true
}

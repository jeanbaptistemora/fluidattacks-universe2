variable "vaultBucket" {}

data "aws_iam_policy_document" "key_access_policy" {
  statement {
    sid     = "Allow Access to EKSNode role"
    actions = ["kms:Encrypt", "kms:Decrypt"]

    principals {
      type        = "AWS"
      identifiers = ["${aws_iam_role.k8s_nodes_role.arn}"]
    }
  }
}

resource "aws_kms_key" "vault_encryption_key" {
  description             = "Key used to encrypt and store Vault unseal key"
  deletion_window_in_days = 7
  policy = "${data.aws_iam_policy_document.key_access_policy.json}"

  tags {
    Name = "Vault_Encryption_Key"
    App  = "Vault"
  }
}

resource "aws_s3_bucket" "vault" {
  bucket = "${var.vaultBucket}"
  acl    = "private"

  lifecycle_rule {
    id      = "cleanup"
    prefix  = "vault.etcd"
    enabled = true
    expiration {
      days  = 30
    }
  }

  tags {
    Name = "Vault_Bucket"
    App  = "Vault"
  }
}

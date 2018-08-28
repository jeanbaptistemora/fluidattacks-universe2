variable "vaultBucket" {}

resource "aws_s3_bucket" "vault_bucket" {
  bucket = "${var.vaultBucket}"
  acl    = "private"
  tags {
    Name = "Vault Backup Bucket"
  }
  lifecycle_rule {
    id      = "cleanup"
    prefix  = "vault.etcd"
    enabled = true
    expiration {
      days  = 30
    }
  }
}

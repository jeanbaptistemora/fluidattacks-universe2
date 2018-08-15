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

resource "aws_iam_user" "vault_user" {
  name = "FluidVault"
  path = "/"
}

resource "aws_iam_access_key" "vault_key" {
  user = "${aws_iam_user.vault_user.name}"  
}

resource "aws_iam_group" "vault_group" {
  name = "FluidVault"
  path = "/"
}

resource "aws_iam_group_membership" "vault_member" {
  name = "VaultMembership"
  users = ["${aws_iam_user.vault_user.name}"]
  group = "${aws_iam_group.vault_group.name}"
}

resource "aws_iam_group_policy" "vault_policy" {
  name   = "VaultS3Policy"
  group  = "${aws_iam_group.vault_group.id}"
  policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": [
        "s3:*"
      ],
      "Effect": "Allow",
      "Resource": [
        "arn:aws:s3:::${var.vaultBucket}",
        "arn:aws:s3:::${var.vaultBucket}/*"
      ]
    }
  ]
}
EOF
}

output "vault_access_key" {
  value = "${aws_iam_access_key.vault_key.id}"
  sensitive = true
}

output "vault_secret_key" {
  value = "${aws_iam_access_key.vault_key.secret}"
  sensitive = true  
}
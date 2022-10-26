# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

variable "clusterUser" {
  default = "fakeUser"
}
variable "clusterPass" {
  default = "fakePassword1234"
}
# IAM
data "aws_iam_policy_document" "cluster-policy-data" {
  statement {
    sid    = "MigrationBucketManagement"
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:GetBucketAcl",
      "s3:GetBucketCors",
      "s3:GetEncryptionConfiguration",
      "s3:GetBucketLocation",
      "s3:ListBucket",
      "s3:ListAllMyBuckets",
      "s3:ListMultipartUploadParts",
      "s3:ListBucketMultipartUploads",
      "s3:PutObject",
      "s3:PutBucketAcl",
      "s3:PutBucketCors",
      "s3:DeleteObject",
      "s3:AbortMultipartUpload",
      "s3:CreateBucket",
    ]
    resources = [
      "arn:aws:s3:::observes.etl-data",
      "arn:aws:s3:::observes.etl-data/*",
    ]
  }
}
data "aws_iam_policy_document" "cluster-assume-role-document" {
  statement {
    sid    = "RedshiftAccess"
    effect = "Allow"
    actions = [
      "sts:AssumeRole"
    ]
    principals {
      type        = "Service"
      identifiers = ["redshift.amazonaws.com"]
    }
  }
}
resource "aws_iam_policy" "redshift-cluster-policy" {
  name        = "redshift-cluster-policy"
  path        = "/"
  description = "Policy for redshift s3 access"
  policy      = data.aws_iam_policy_document.cluster-policy-data.json
}
resource "aws_iam_role" "redshift-role" {
  name               = "redshift-role"
  assume_role_policy = data.aws_iam_policy_document.cluster-assume-role-document.json
  tags = {
    "Name"               = "redshift-role"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}
resource "aws_iam_role_policy_attachment" "redshift-role-cluster-policy" {
  role       = aws_iam_role.redshift-role.name
  policy_arn = aws_iam_policy.redshift-cluster-policy.arn
}
resource "aws_iam_role_policy_attachment" "redshift-role-default-redshift-policy" {
  role       = aws_iam_role.redshift-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonRedshiftAllCommandsFullAccess"
}
# Network
resource "aws_security_group" "expose-redshift" {
  name        = "expose-redshift"
  description = "Expose redshift endpoint"
  vpc_id      = data.aws_vpc.main.id
  ingress {
    description      = "External access"
    from_port        = 5439
    to_port          = 5439
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  egress {
    description      = "VPC access"
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  tags = {
    "Name"               = "observes"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}
resource "aws_redshift_subnet_group" "main" {
  name = "observes"
  subnet_ids = [
    for subnet in data.aws_subnet.main : subnet.id
  ]

  tags = {
    "Name"               = "observes"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}
# Cluster
resource "aws_redshift_cluster" "main" {
  cluster_identifier = "observes"
  database_name      = "observes"
  master_username    = var.clusterUser
  master_password    = var.clusterPass

  cluster_type    = "multi-node"
  node_type       = "dc2.large"
  number_of_nodes = 2

  publicly_accessible  = true
  encrypted            = true
  enhanced_vpc_routing = true

  cluster_subnet_group_name = aws_redshift_subnet_group.main.name
  vpc_security_group_ids    = [aws_security_group.expose-redshift.id]

  preferred_maintenance_window        = "sun:04:00-sun:05:00"
  automated_snapshot_retention_period = 7
  iam_roles                           = [aws_iam_role.redshift-role.arn]

  tags = {
    "Name"               = "observes"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}

variable "ci_cache_buckets" {
  default = {
    autoscaling_ci_cache   = "autoscaling-ci-cache",
    autonomicmind_ci_cache = "autonomicmind-ci-cache",
    autonomicjump_ci_cache = "autonomicjump-ci-cache",
  }
}

data "aws_iam_policy_document" "autoscaling_ci_policy_document_data" {

  # https://docs.gitlab.com/runner/configuration/runner_autoscale_aws/index.html#aws-credentials

  statement {
    sid    = "AutoscalingCIFullEC2Access"
    effect = "Allow"
    actions = [
      "ec2:*"
    ]
    resources = [
      "*"
    ]
  }

  statement {
    sid    = "AutoscalingCIFullS3CacheAccess"
    effect = "Allow"
    actions = [
      "s3:*"
    ]
    resources = [
      "arn:aws:s3:::autoscaling-ci-cache/*",
      "arn:aws:s3:::autonomicmind-ci-cache/*",
      "arn:aws:s3:::autonomicjump-ci-cache/*",
    ]
  }

}

resource "aws_iam_policy" "autoscaling_ci_policy" {
  name        = "autoscaling-ci-policy"
  path        = "/autoscaling-ci/"
  description = "Policy to allow the Bastion to manage EC2 and S3 Cache bucket"

  policy = data.aws_iam_policy_document.autoscaling_ci_policy_document_data.json
}

resource "aws_iam_user" "autoscaling_ci_user" {
  name = "autoscaling-ci"
  path = "/autoscaling-ci/"

  tags = {
    "Name"               = "autoscaling-ci"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_user_policy_attachment" "attach_autoscaling_ci_policy" {
  policy_arn = aws_iam_policy.autoscaling_ci_policy.arn
  user       = aws_iam_user.autoscaling_ci_user.name
}

resource "aws_s3_bucket" "ci_cache_buckets" {

  for_each = var.ci_cache_buckets

  bucket        = each.value
  acl           = "private"
  force_destroy = true

  versioning {
    enabled = false
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    "Name"               = each.value
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_security_group" "autoscaling_ci_security_group_2" {
  name        = "AutoscalingCISG"
  description = "Docker Machine"
  vpc_id      = var.autostaling_ci_vpc_id

  ingress {
    description = "ssh-access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = []
    self        = true
  }

  ingress {
    description = "docker-access"
    from_port   = 2376
    to_port     = 2376
    protocol    = "tcp"
    cidr_blocks = []
    self        = true
  }

  egress {
    description = "default-aws-egress-rule"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name"               = "AutoscalingCISG"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

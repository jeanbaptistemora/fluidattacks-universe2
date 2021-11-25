data "aws_iam_policy_document" "skims_prod_policy_data" {
  # S3 access to the terraform state and Airs bucket
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:GetObject",
      "s3:PutObject",
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod/skims.tfstate",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:DeleteObject",
      "s3:GetObject",
      "s3:PutObject",
      "s3:ListBucket",
    ]
    resources = [
      "arn:aws:s3:::fluidattacks.com",
      "arn:aws:s3:::fluidattacks.com/resources/doc/skims/*",
    ]
  }

  # IAM and AWS SSO role
  statement {
    effect = "Allow"
    actions = [
      "iam:*",
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:instance-profile/skims_*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user_provision/skims_*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/skims_*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/skims_*",
    ]
  }

  # Batch access
  statement {
    effect  = "Allow"
    actions = ["batch:SubmitJob"]
    resources = [
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-definition/*",
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/dedicated*",
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/skims*",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "batch:ListJobs",
      "batch:DescribeJobDefinitions",
      "batch:DescribeJobQueues",
      "batch:DescribeComputeEnvironments",
      "batch:DescribeJobs",
    ]
    resources = ["*"]
  }

  # CloudWatch
  statement {
    effect = "Allow"
    actions = [
      "logs:DescribeLogGroups",
      "logs:FilterLogEvents ",
      "logs:GetLogEvents",
    ]
    resources = [
      "arn:aws:logs:us-east-1:${data.aws_caller_identity.current.account_id}:log-group:/aws/batch/job:log-stream:*",
    ]
  }

  # EC2
  statement {
    effect = "Allow"
    actions = [
      "ec2:ApplySecurityGroupsToClientVpnTargetNetwork",
      "ec2:AuthorizeSecurityGroupEgress",
      "ec2:AuthorizeSecurityGroupIngress",
      "ec2:Create*",
      "ec2:Describe*",
      "ec2:DeleteSecurityGroup",
      "ec2:DeleteSubnet",
      "ec2:DeleteTags",
      "ec2:DeleteNetworkInterface",
      "ec2:ModifySubnetAttribute",
      "ec2:RevokeSecurityGroupEgress",
      "ec2:RevokeSecurityGroupIngress",
      "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
      "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
    ]
    resources = ["*"]
  }

  # KMS
  statement {
    effect = "Allow"
    actions = [
      "kms:CreateKey",
      "kms:ListAliases",
    ]
    resources = [
      "*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "kms:*"
    ]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:key/*"
    ]
    condition {
      test     = "ForAnyValue:StringEquals"
      variable = "kms:ResourceAliases"

      values = [
        "alias/skims_prod",
        "alias/skims_dev",
      ]
    }
  }

  # S3 admin over skims buckets
  statement {
    effect = "Allow"
    actions = [
      "s3:*",
    ]
    resources = [
      "arn:aws:s3:::skims.*"
    ]
  }

  # DynamoDB for locking terraform state
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:DeleteItem",
      "dynamodb:GetItem",
      "dynamodb:PutItem",
    ]
    resources = [
      var.terraform_state_lock_arn,
    ]
  }
}

resource "aws_iam_policy" "skims_prod_policy" {
  description = "skims_prod policy"
  name        = "skims_prod_policy"
  path        = "/user_provision/"
  policy      = data.aws_iam_policy_document.skims_prod_policy_data.json
}

resource "aws_iam_user_policy_attachment" "skims_prod_attach_policy" {
  user       = "skims_prod"
  policy_arn = aws_iam_policy.skims_prod_policy.arn
}

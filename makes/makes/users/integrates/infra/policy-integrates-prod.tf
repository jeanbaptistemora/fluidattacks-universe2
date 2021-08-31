data "aws_iam_policy_document" "integrates-prod-policy-data" {

  # S3
  statement {
    effect  = "Allow"
    actions = ["s3:*"]
    resources = [
      "arn:aws:s3:::fluidintegrates*/*",
      "arn:aws:s3:::fluidintegrates*",
      "arn:aws:s3:::integrates*/*",
      "arn:aws:s3:::integrates*",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/*",
    ]
  }

  # IAM
  statement {
    effect = "Allow"
    actions = [
      "iam:List*",
      "iam:Get*",
      "iam:Create*",
    ]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["iam:*"]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/integrates-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/integrates-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:instance-profile/integrates-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:oidc-provider/*",
    ]
  }
  statement {
    effect  = "Allow"
    actions = ["iam:PassRole"]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/aws-service-role/dynamodb.application-autoscaling.amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable"
    ]
  }

  # EC2
  statement {
    effect = "Allow"
    actions = [
      "ec2:Describe*",
      "ec2:DeleteSubnet",
      "ec2:DeleteNetworkInterface",
      "ec2:ModifySubnetAttribute",
      "ec2:CreateSubnet",
      "ec2:CreateLaunchTemplate",
      "ec2:CreateLaunchTemplateVersion",
      "ec2:DeleteLaunchTemplate",
      "ec2:ModifyLaunchTemplate",
      "ec2:DeleteLaunchTemplateVersions",
      "ec2:CreateTags",
      "ec2:DeleteTags",
      "ec2:ApplySecurityGroupsToClientVpnTargetNetwork",
      "ec2:AuthorizeSecurityGroupEgress",
      "ec2:AuthorizeSecurityGroupIngress",
      "ec2:CreateSecurityGroup",
      "ec2:DeleteSecurityGroup",
      "ec2:RunInstances",
      "ec2:RevokeSecurityGroupEgress",
      "ec2:RevokeSecurityGroupIngress",
      "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
      "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
    ]
    resources = ["*"]
  }

  # Elasticache
  statement {
    effect = "Allow"
    actions = [
      "elasticache:Describe*",
      "elasticache:List*",
      "elasticache:CreateReplicationGroup",
      "elasticache:CreateCacheSecurityGroup",
      "elasticache:CreateCacheSubnetGroup",
      "elasticache:AddTagsToResource",
    ]
    resources = ["*"]
  }
  statement {
    effect = "Allow"
    actions = [
      "elasticache:*",
    ]
    resources = [
      "arn:aws:elasticache:${var.region}:${data.aws_caller_identity.current.account_id}:subnetgroup:integrates-*",
      "arn:aws:elasticache:${var.region}:${data.aws_caller_identity.current.account_id}:replicationgroup:integrates-*",
    ]
  }

  # Lambda
  statement {
    effect  = "Allow"
    actions = ["lambda:*"]
    resources = [
      "arn:aws:lambda:${var.region}:${data.aws_caller_identity.current.account_id}:function:integrates-*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "lambda:UpdateEventSourceMapping",
      "lambda:ListEventSourceMappings",
      "lambda:GetEventSourceMapping",
      "lambda:DeleteEventSourceMapping",
      "lambda:CreateEventSourceMapping"
    ]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["logs:*"]
    resources = [
      "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/lambda/integrates-*"
    ]
  }

  # KMS
  statement {
    effect = "Allow"
    actions = [
      "kms:UntagResource",
      "kms:TagResource",
      "kms:List*",
      "kms:Get*",
      "kms:Describe*",
      "kms:CreateKey",
      "kms:CreateAlias",
      "kms:DeleteAlias",
      "kms:UpdateAlias",
    ]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["kms:*"]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/integrates-prod-*"
    ]
  }

  # Kubernetes autoscaling
  statement {
    effect = "Allow"
    actions = [
      "application-autoscaling:RegisterScalableTarget",
      "application-autoscaling:PutScalingPolicy",
      "application-autoscaling:DescribeScalingPolicies",
      "application-autoscaling:DescribeScalingActivities",
      "application-autoscaling:DescribeScalableTargets",
      "application-autoscaling:DeregisterScalableTarget",
      "application-autoscaling:DeleteScalingPolicy"
    ]
    resources = ["*"]
  }

  # Others
  statement {
    effect    = "Allow"
    actions   = ["sqs:*"]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["cloudwatch:*"]
    resources = [
      "arn:aws:cloudwatch:${var.region}:${data.aws_caller_identity.current.account_id}:alarm:fi*"
    ]
  }
  statement {
    effect    = "Allow"
    actions   = ["cloudfront:*"]
    resources = ["*"]
  }

  # ACM create and read certificate
  statement {
    effect = "Allow"
    actions = [
      "acm:RequestCertificate",
      "acm:DescribeCertificate",
      "acm:ListTagsForCertificate",
      "acm:AddTagsToCertificate",
      "acm:DeleteCertificate",
    ]
    resources = [
      "*",
    ]
  }

  # S3 read over continuous data buckets
  statement {
    sid    = "s3ContinuousDataRead"
    effect = "Allow"
    actions = [
      "s3:Get*",
      "s3:ListBucket"
    ]
    resources = [
      "arn:aws:s3:::continuous-data",
      "arn:aws:s3:::continuous-data/*",
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

  # EKS full permissions over owned resources
  statement {
    effect = "Allow"
    actions = [
      "eks:Describe*",
      "eks:List*",
      "eks:Create*",
    ]
    resources = ["*"]
  }
  statement {
    effect = "Allow"
    actions = [
      "eks:*"
    ]
    resources = ["arn:aws:eks:${var.region}:${data.aws_caller_identity.current.account_id}:cluster/integrates-*"]
  }

  # Autoscaling read/write permissions over owned resources
  statement {
    effect = "Allow"
    actions = [
      "autoscaling:Create*",
      "autoscaling:Describe*",
      "autoscaling:Get*",
    ]
    resources = ["*"]
  }
  statement {
    effect = "Allow"
    actions = [
      "autoscaling:*"
    ]
    resources = [
      "arn:aws:autoscaling:${var.region}:${data.aws_caller_identity.current.account_id}:launchConfiguration:*:launchConfigurationName/integrates-*",
      "arn:aws:autoscaling:${var.region}:${data.aws_caller_identity.current.account_id}:autoScalingGroup:*:autoScalingGroupName/integrates-*",
    ]
  }

  # WAF read/write permissions over owned resources
  statement {
    effect = "Allow"
    actions = [
      "wafv2:Describe*",
      "wafv2:List*",
      "wafv2:Get*",
      "wafv2:Check*",
      "wafv2:CreateWebACL",
    ]
    resources = ["*"]
  }
  statement {
    effect = "Allow"
    actions = [
      "wafv2:*",
    ]
    resources = [
      "arn:aws:wafv2:${var.region}:${data.aws_caller_identity.current.account_id}:regional/webacl/integrates-*",
      "arn:aws:wafv2:${var.region}:${data.aws_caller_identity.current.account_id}:regional/managedruleset/*",
    ]
  }

  # Batch access
  statement {
    effect    = "Allow"
    actions   = ["batch:ListJobs"]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["batch:SubmitJob"]
    resources = [
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-definition/default",
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/spot*",
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/dedicated_soon",
      "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/dedicated_later",
    ]
  }
}

resource "aws_iam_policy" "integrates-prod-policy" {
  description = "integrates-prod policy"
  name        = "integrates-prod-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-prod-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy" {
  user       = "integrates-prod"
  policy_arn = aws_iam_policy.integrates-prod-policy.arn
}

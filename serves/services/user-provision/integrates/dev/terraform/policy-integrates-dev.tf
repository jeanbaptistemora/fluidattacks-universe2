data "aws_iam_policy_document" "integrates-dev-policy-data" {

  # S3
  statement {
    effect  = "Allow"
    actions = ["s3:*"]
    resources = [
      "arn:aws:s3:::fluidintegrates*/*",
      "arn:aws:s3:::fluidintegrates*",
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
      "arn:aws:s3:::servestf/integrates.tfstate",
      "arn:aws:s3:::servestf",
      "arn:aws:s3:::fluidattacks-terraform-states-dev",
      "arn:aws:s3:::fluidattacks-terraform-states-dev/*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-prod",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/*"
    ]
  }

  # IAM
  statement {
    effect = "Allow"
    actions = [
      "iam:List*",
      "iam:Get*"
    ]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["iam:*"]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/integrates-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/integrates-*"
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
      "ec2:DescribeSubnets",
      "ec2:DescribeSecurityGroupReferences",
      "ec2:DescribeSecurityGroups",
      "ec2:DescribeStaleSecurityGroups",
    ]
    resources = ["*"]
  }

  # Elasticache
  statement {
    effect = "Allow"
    actions = [
      "elasticache:Describe*",
      "elasticache:List*"
    ]
    resources = ["*"]
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
      "kms:UpdateAlias"
    ]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = ["kms:*"]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/integrates-dev-*"
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
      "application-autoscaling:DeleteScalingPolicy",
    ]
    resources = ["*"]
  }

  # Autoscaling read
  statement {
    effect = "Allow"
    actions = [
      "autoscaling:DescribeLaunchConfigurations",
      "autoscaling:DescribeAutoScalingGroups"
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
  statement {
    effect  = "Allow"
    actions = [
      "devicefarm:ListProjects",
    ]
    resources = ["*"]
  }
  statement {
    effect  = "Allow"
    actions = [
      "devicefarm:CreateDevicePool",
      "devicefarm:CreateUpload",
      "devicefarm:GetProject",
      "devicefarm:GetRun",
      "devicefarm:GetUpload",
      "devicefarm:ListArtifacts",
      "devicefarm:ListJobs",
      "devicefarm:ScheduleRun",
    ]
    resources = [
      "arn:aws:devicefarm:us-west-2:${data.aws_caller_identity.current.account_id}:devicepool:*",
      "arn:aws:devicefarm:us-west-2:${data.aws_caller_identity.current.account_id}:job:*",
      "arn:aws:devicefarm:us-west-2:${data.aws_caller_identity.current.account_id}:project:*",
      "arn:aws:devicefarm:us-west-2:${data.aws_caller_identity.current.account_id}:run:*",
      "arn:aws:devicefarm:us-west-2:${data.aws_caller_identity.current.account_id}:upload:*",
    ]
  }

  # ACM create and read certificate
  statement {
    effect  = "Allow"
    actions = [
      "acm:RequestCertificate",
      "acm:DescribeCertificate",
      "acm:ListTagsForCertificate",
    ]
    resources = [
      "*",
    ]
  }

  # Route 53 basic read
  statement {
    effect  = "Allow"
    actions = [
      "route53:ListHostedZones",
      "route53:GetHostedZone",
      "route53:GetChange"
    ]
    resources = [
      "*",
    ]
  }

  # Route 53 read/write over fluidattacks hosted zone
  statement {
    effect  = "Allow"
    actions = [
      "route53:ListTagsForResource",
      "route53:ListResourceRecordSets"
    ]
    resources = [
      "arn:aws:route53:::hostedzone/${data.aws_route53_zone.fluidattacks.zone_id}",
    ]
  }

  # S3 read over continuous data buckets
  statement {
    sid = "s3ContinuousDataRead"
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

  # EKS read permissions
  statement {
    effect = "Allow"
    actions = [
      "eks:Describe*",
      "eks:List*",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "integrates-dev-policy" {
  description = "integrates-dev policy"
  name        = "${var.user-name}-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-dev-policy-data.json
}

resource "aws_iam_user_policy_attachment" "integrates-dev-attach-policy" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-dev-policy.arn
}

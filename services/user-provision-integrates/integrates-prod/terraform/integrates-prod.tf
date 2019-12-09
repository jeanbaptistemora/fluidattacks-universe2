data "aws_iam_policy_document" "integrates-prod-policy-data" {
  statement {
    effect  = "Allow"
    actions = ["s3:*"]
    resources = [
      "arn:aws:s3:::fluidintegrates*/*",
      "arn:aws:s3:::fluidintegrates*",
      "arn:aws:s3:::fi.binaryalert*"
    ]
  }
  statement {
    effect    = "Allow"
    actions   = ["s3:ListBucket"]
    resources = ["arn:aws:s3:::fluidattacks-terraform-states-prod"]
  }
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = ["arn:aws:s3:::fluidattacks-terraform-states-prod"]
  }
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:DescribeLogGroups",
      "logs:DescribeLogStreams",
      "logs:PutLogEvents",
      "logs:GetLogEvents",
      "logs:FilterLogEvents"
    ]
  }
  statement {
    effect    = "Allow"
    actions   = ["cloudfront:*"]
    resources = ["*"]
  }
  statement {
    effect = "Allow"
    actions = [
      "application-autoscaling:DeleteScalingPolicy",
      "application-autoscaling:DeregisterScalableTarget",
      "application-autoscaling:DescribeScalableTargets",
      "application-autoscaling:DescribeScalingActivities",
      "application-autoscaling:DescribeScalingPolicies",
      "application-autoscaling:PutScalingPolicy",
      "application-autoscaling:RegisterScalableTarget",
      "cloudwatch:DeleteAlarms",
      "cloudwatch:DescribeAlarmHistory",
      "cloudwatch:DescribeAlarms",
      "cloudwatch:DescribeAlarmsForMetric",
      "cloudwatch:GetMetricStatistics",
      "cloudwatch:ListMetrics",
      "cloudwatch:PutMetricAlarm",
      "datapipeline:ActivatePipeline",
      "datapipeline:CreatePipeline",
      "datapipeline:DeletePipeline",
      "datapipeline:DescribeObjects",
      "datapipeline:DescribePipelines",
      "datapipeline:GetPipelineDefinition",
      "datapipeline:ListPipelines",
      "datapipeline:PutPipelineDefinition",
      "datapipeline:QueryObjects",
      "ec2:DescribeVpcs",
      "ec2:DescribeSubnets",
      "ec2:DescribeSecurityGroups",
      "iam:GetRole",
      "iam:ListRoles",
      "kms:DescribeKey",
      "kms:ListAliases",
      "sns:CreateTopic",
      "sns:DeleteTopic",
      "sns:ListSubscriptions",
      "sns:ListSubscriptionsByTopic",
      "sns:ListTopics",
      "sns:Subscribe",
      "sns:Unsubscribe",
      "sns:SetTopicAttributes",
      "lambda:CreateFunction",
      "lambda:ListFunctions",
      "lambda:ListEventSourceMappings",
      "lambda:CreateEventSourceMapping",
      "lambda:DeleteEventSourceMapping",
      "lambda:GetFunctionConfiguration",
      "lambda:DeleteFunction",
      "resource-groups:ListGroups",
      "resource-groups:ListGroupResources",
      "resource-groups:GetGroup",
      "resource-groups:GetGroupQuery",
      "resource-groups:DeleteGroup",
      "resource-groups:CreateGroup",
      "tag:GetResources"
    ]
    resources = [
      "arn:aws:dynamodb:${var.region}:${data.aws_caller_identity.current.account_id}:table/fi*",
      "arn:aws:dynamodb:${var.region}:${data.aws_caller_identity.current.account_id}:table/FI*"
    ]
  }
}

resource "aws_iam_policy" "integrates-prod-policy" {
  description = "Integrates policy for ${aws_iam_user.integrates-prod.name}"
  name        = "user-provision-policy-${aws_iam_user.integrates-prod.name}"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-prod-policy-data.json
}

resource "aws_iam_user" "integrates-prod" {
  name = "integrates-prod"
  path = "/user-provision/"
}

resource "aws_iam_access_key" "integrates-prod-key" {
  user = aws_iam_user.integrates-prod.name
}

resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy" {
  user       = aws_iam_user.integrates-prod.name
  policy_arn = aws_iam_policy.integrates-prod-policy.arn
}

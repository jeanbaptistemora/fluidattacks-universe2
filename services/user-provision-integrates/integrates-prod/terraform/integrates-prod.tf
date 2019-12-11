data "aws_iam_policy_document" "integrates-prod-policy-data" {
  /* Policy to allow permissions for integrates-prod needs, here will be any permission or restriction
  needed for integrates-prod user */
  statement {
    # S3 Full permissions for storing Integrates data
    effect  = "Allow"
    actions = ["s3:*"]
    resources = [
      "arn:aws:s3:::fluidintegrates*/*",
      "arn:aws:s3:::fluidintegrates*",
      "arn:aws:s3:::fi.binaryalert*"
    ]
  }
  statement {
    # S3 List permissions necessarries to check if terraformm backend exists
    effect    = "Allow"
    actions   = ["s3:ListBucket"]
    resources = ["arn:aws:s3:::fluidattacks-terraform-states-prod"]
  }
  statement {
    /* S3 Read/Write permissions necessaries to check if tfstate exists and if not,
        then create it */
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = ["arn:aws:s3:::fluidattacks-terraform-states-prod"]
  }
  statement {
    # Cloudwatch logs permissions for monitoring
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
    resources = ["*"]
  }
  statement {
    effect    = "Allow"
    actions   = ["cloudfront:*"]
    resources = ["*"]
  }
  statement {
    # DynamoDBFullAccess permisisons to do any required operations in the database
    effect = "Allow"
    actions = [
      "dax:*",
      "sqs:*",
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
    resources = ["*"]
  }
  statement {
    # Allow DynamoDb operations only in theese tables(resources)
    effect  = "Allow"
    actions = ["dynamodb:*"]
    resources = [
      "arn:aws:dynamodb:${var.region}:${data.aws_caller_identity.current.account_id}:table/fi*",
      "arn:aws:dynamodb:${var.region}:${data.aws_caller_identity.current.account_id}:table/FI*"
    ]
  }
  statement {
    # Restrict users to pass roles only to the specified service
    effect  = "Allow"
    actions = ["iam:PassRole"]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/aws-service-role/dynamodb.application-autoscaling.amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable"
    ]
  }
  statement {
    # Allow users to pass roles only if the role arn passed to service as principal matches values
    effect    = "Allow"
    actions   = ["iam:PassRole"]
    resources = ["*"]
    condition {
      test     = "StringLike"
      variable = "iam:PassedToService"
      values = [
        "application-autoscaling.amazonaws.com",
        "dax.amazonaws.com"
      ]
    }
  }
  statement {
    # DynamoDBFullAccess Permissions
    effect    = "Allow"
    actions   = ["iam:CreateServiceLinkedRole"]
    resources = ["*"]
    condition {
      test     = "StringEquals"
      variable = "iam:AWSServiceName"
      values = [
        "replication.dynamodb.amazonaws.com",
        "dax.amazonaws.com",
        "dynamodb.application-autoscaling.amazonaws.com",
        "contributorinsights.dynamodb.amazonaws.com"
      ]
    }
  }
  statement {
    # Allows any cloudwatch operation in theese resources for analysis monitoring
    effect  = "Allow"
    actions = ["cloudwatch:*"]
    resources = [
      "arn:aws:cloudwatch:${var.region}:${data.aws_caller_identity.current.account_id}:alarm:fi*",
      "arn:aws:cloudwatch::${data.aws_caller_identity.current.account_id}:dashboard/BinaryAlert"
    ]
  }
  statement {
    # EventsLog
    effect  = "Allow"
    actions = ["events:*"]
    resources = [
      "arn:aws:events:${var.region}:${data.aws_caller_identity.current.account_id}:rule/fi_binaryalert"
    ]
  }
  statement {
    # IAMRead
    effect = "Allow"
    actions = [
      "iam:List*",
      "iam:Get*"
    ]
    resources = ["*"]
  }
  statement {
    # FunctionRoles
    effect  = "Allow"
    actions = ["iam:*"]
    resources = [
      "arn:aws:iam::205810638802:role/integrates-*",
      "arn:aws:iam::205810638802:role/fi_binaryalert*",
      "arn:aws:iam::205810638802:policy/integrates-*",
      "arn:aws:iam::205810638802:policy/fi_binaryalert*"
    ]
  }
  statement {
    # QueueKeyCreation
    effect = "Allow"
    actions = [
      "kms:UntagResource",
      "kms:TagResource",
      "kms:List*",
      "kms:Get*",
      "kms:Describe*",
      "kms:CreateKey"
    ]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/integrates-prod-*"
    ]
  }
  statement {
    # QueueEncryption
    effect  = "Allow"
    actions = ["kms:*"]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/fi_binaryalert*"
    ]
  }
  statement {
    # LambdaCreateMapping
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
    # AnalysisFunctions and LambdaFunctions
    effect  = "Allow"
    actions = ["lambda:*"]
    resources = [
      "arn:aws:lambda:${var.region}:${data.aws_caller_identity.current.account_id}:function:fi_binaryalert*",
      "arn:aws:lambda:${var.region}:${data.aws_caller_identity.current.account_id}:function:integrates-*"
    ]
  }
  statement {
    # LogsList
    effect = "Allow"
    actions = [
      "logs:List*",
      "logs:Describe*"
    ]
    resources = ["*"]
  }
  statement {
    # FunctionLogs
    effect  = "Allow"
    actions = ["logs:*"]
    resources = [
      "arn:aws:lambda:${var.region}:${data.aws_caller_identity.current.account_id}:function:fi_binaryalert*",
      "arn:aws:lambda:${var.region}:${data.aws_caller_identity.current.account_id}:function:integrates-*"
    ]
  }
  statement {
    # ResultsNotification
    effect  = "Allow"
    actions = ["sns:*"]
    resources = [
      "arn:aws:sns:${var.region}:${data.aws_caller_identity.current.account_id}:function:fi_binaryalert*"
    ]
  }
  statement {
    # AnalysisQueue
    effect    = "Allow"
    actions   = ["sqs:*"]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "integrates-prod-policy" {
  description = "Integrates policy for ${var.user-name}"
  name        = "user-provision-policy-${var.user-name}"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.integrates-prod-policy-data.json
}

resource "aws_iam_user" "integrates-prod" {
  name = "integrates-prod"
  path = "/user-provision/"
}

resource "aws_iam_access_key" "integrates-prod-key" {
  user = var.user-name
}

resource "aws_iam_user_policy_attachment" "integrates-prod-attach-policy" {
  user       = var.user-name
  policy_arn = aws_iam_policy.integrates-prod-policy.arn
}

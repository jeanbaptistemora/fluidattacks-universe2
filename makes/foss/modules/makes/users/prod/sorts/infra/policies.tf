locals {
  aws = {
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "batchRead"
        Effect = "Allow"
        Action = [
          "batch:DescribeComputeEnvironments",
          "batch:DescribeJobDefinitions",
          "batch:DescribeJobQueues",
          "batch:DescribeJobs",
          "batch:ListJobs",
        ]
        Resource = ["*"]
      },
      {
        Sid    = "batchWrite"
        Effect = "Allow"
        Action = [
          "batch:SubmitJob",
        ]
        Resource = [
          "arn:aws:batch:${var.region}:${data.aws_caller_identity.current.account_id}:job-definition/*",
          "arn:aws:batch:${var.region}:${data.aws_caller_identity.current.account_id}:job-queue/spot*",
          "arn:aws:batch:${var.region}:${data.aws_caller_identity.current.account_id}:job-queue/dedicated*",
        ]
      },
      {
        Sid    = "logsRead"
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:Describe*",
          "logs:Filter*",
          "logs:Get*",
          "logs:List*",
        ]
        Resource = ["*"]
      },
      {
        Sid    = "logsWrite"
        Effect = "Allow"
        Action = ["*"]
        Resource = [
          "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/sagemaker/TrainingJobs",
          "arn:aws:logs:${var.region}:${data.aws_caller_identity.current.account_id}:log-group:/aws/sagemaker/TrainingJobs:log-stream:*",
        ]
      },
      {
        Sid    = "redshiftRead"
        Effect = "Allow"
        Action = [
          "redshift-data:*",
          "redshift:Describe*",
        ]
        Resource = ["*"]
      },
      {
        Sid    = "redshiftWrite"
        Effect = "Allow"
        Action = ["*"]
        Resource = [
          "arn:aws:redshift:${var.region}:${data.aws_caller_identity.current.account_id}:cluster:fluid-redshift",
          "arn:aws:redshift:${var.region}:${data.aws_caller_identity.current.account_id}:dbname:fluid-redshift/*",
          "arn:aws:redshift:${var.region}:${data.aws_caller_identity.current.account_id}:dbuser:fluid-redshift/*",
        ]
      },
      {
        Sid    = "s3Write"
        Effect = "Allow"
        Action = ["*"]
        Resource = [
          "arn:aws:s3:::fluidattacks-terraform-states-prod/sorts*",
          "arn:aws:s3:::sorts",
          "arn:aws:s3:::sorts/*",
        ]
      },
      {
        Sid    = "sagemakerRead"
        Effect = "Allow"
        Action = [
          "sagemaker:List*",
        ]
        Resource = ["*"]
      },
      {
        Sid    = "sagemakerWrite"
        Effect = "Allow"
        Action = ["*"]
        Resource = [
          "arn:aws:sagemaker:${var.region}:${data.aws_caller_identity.current.account_id}:hyper-parameter-tuning-job/sagemaker*",
          "arn:aws:sagemaker:${var.region}:${data.aws_caller_identity.current.account_id}:training-job/sagemaker*",
          "arn:aws:sagemaker:${var.region}:${data.aws_caller_identity.current.account_id}:training-job/sorts*",
        ]
      },
      {
        Sid    = "costmanagementRead"
        Effect = "Allow"
        Action = [
          "aws-portal:View*",
          "ce:Describe*",
          "ce:List*",
          "cur:Describe*",
        ]
        Resource = ["*"]
      },
      {
        Sid    = "kmsRead"
        Effect = "Allow"
        Action = [
          "kms:CreateAlias",
          "kms:CreateKey",
          "kms:Describe*",
          "kms:Get*",
          "kms:List*",
          "kms:TagResource",
          "kms:UntagResource",
          "kms:UpdateAlias",
        ]
        Resource = ["*"]
      },
      {
        Sid    = "dynamoWrite"
        Effect = "Allow"
        Action = [
          "dynamodb:DeleteItem",
          "dynamodb:GetItem",
          "dynamodb:PutItem",
        ]
        Resource = [
          var.terraform_state_lock_arn,
        ]
      },
    ]
  }
}

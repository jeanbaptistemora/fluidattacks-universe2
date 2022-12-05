locals {
  prod_sorts = {
    policies = {
      aws = [
        {
          Sid    = "dynamoRead"
          Effect = "Allow"
          Action = [
            "dynamodb:BatchGet*",
            "dynamodb:Describe*",
            "dynamodb:Get*",
            "dynamodb:List*",
            "dynamodb:Query*",
            "dynamodb:Scan*",
          ]
          Resource = ["*"]
        },
        {
          Sid    = "batchRead"
          Effect = "Allow"
          Action = [
            "batch:Describe*",
            "batch:List*",
          ]
          Resource = ["*"]
        },
        {
          Sid    = "batchWrite"
          Effect = "Allow"
          Action = [
            "batch:CancelJob",
            "batch:SubmitJob",
            "batch:TerminateJob",
          ]
          Resource = [
            "arn:aws:batch:${var.region}:${data.aws_caller_identity.main.account_id}:job-definition/*",
            "arn:aws:batch:${var.region}:${data.aws_caller_identity.main.account_id}:job-queue/*",
          ]
        },
        {
          Sid    = "cloudwatchRead"
          Effect = "Allow"
          Action = [
            "cloudwatch:Describe*",
            "cloudwatch:Get*",
            "cloudwatch:List*",
          ]
          Resource = ["*"]
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
            "arn:aws:logs:${var.region}:${data.aws_caller_identity.main.account_id}:log-group:/aws/sagemaker/TrainingJobs",
            "arn:aws:logs:${var.region}:${data.aws_caller_identity.main.account_id}:log-group:/aws/sagemaker/TrainingJobs:log-stream:*",
          ]
        },
        {
          Sid    = "redshiftRead"
          Effect = "Allow"
          Action = [
            "redshift-data:Get*",
            "redshift-data:List*",
            "redshift-data:Describe*",
            "redshift:Describe*",
          ]
          Resource = [
            "arn:aws:redshift:${var.region}:${data.aws_caller_identity.main.account_id}:cluster:observes",
          ]
        },
        {
          Sid    = "redshiftWrite"
          Effect = "Allow"
          Action = [
            "redshift:*",
            "redshift-data:*",
          ]
          Resource = [
            "arn:aws:redshift:${var.region}:${data.aws_caller_identity.main.account_id}:cluster:observes",
            "arn:aws:redshift:${var.region}:${data.aws_caller_identity.main.account_id}:dbname:observes/*",
            "arn:aws:redshift:${var.region}:${data.aws_caller_identity.main.account_id}:dbuser:observes/*",
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
            "arn:aws:sagemaker:${var.region}:${data.aws_caller_identity.main.account_id}:hyper-parameter-tuning-job/sagemaker*",
            "arn:aws:sagemaker:${var.region}:${data.aws_caller_identity.main.account_id}:training-job/sagemaker*",
            "arn:aws:sagemaker:${var.region}:${data.aws_caller_identity.main.account_id}:training-job/sorts*",
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
        {
          Sid    = "batchTags"
          Effect = "Allow"
          Action = [
            "batch:TagResource",
            "batch:UntagResource",
          ]
          Resource = [
            "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job-queue/*",
            "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job-definition/*",
            "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job/*",
          ]
          "Condition" : { "StringEquals" : { "aws:RequestTag/management:product" : "sorts" } }
        },
      ]
    }

    keys = {
      prod_sorts = {
        admins = [
          "prod_common",
        ]
        users = [
          "prod_sorts",
        ]
        tags = {
          "Name"               = "prod_sorts"
          "management:area"    = "cost"
          "management:product" = "common"
          "management:type"    = "product"
        }
      }
    }
  }
}

module "prod_sorts_aws" {
  source = "./modules/aws"

  name   = "prod_sorts"
  policy = local.prod_sorts.policies.aws

  assume_role_policy = [
    {
      Sid    = "SageMakerAssumeRolePolicy",
      Effect = "Allow",
      Principal = {
        Service = "sagemaker.amazonaws.com",
      },
      Action = "sts:AssumeRole",
    },
  ]

  tags = {
    "Name"               = "prod_sorts"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

module "prod_sorts_keys" {
  source   = "./modules/key"
  for_each = local.prod_sorts.keys

  name   = each.key
  admins = each.value.admins
  users  = each.value.users
  tags   = each.value.tags
}

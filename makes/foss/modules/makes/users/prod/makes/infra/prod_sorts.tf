locals {
  prod_sorts = {
    policies = {
      aws = {
        Version = "2012-10-17"
        Statement = [
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
              "batch:SubmitJob",
            ]
            Resource = [
              "arn:aws:batch:${var.region}:${data.aws_caller_identity.current.account_id}:job-definition/*",
              "arn:aws:batch:${var.region}:${data.aws_caller_identity.current.account_id}:job-queue/spot*",
              "arn:aws:batch:${var.region}:${data.aws_caller_identity.current.account_id}:job-queue/dedicated*",
            ]
          },
          {
            Sid    = "iamWrite"
            Effect = "Allow"
            Action = ["*"]
            Resource = [
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:instance-profile/*sorts*",
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/*sorts*",
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

    keys = {
      prod_sorts = {
        admins = [
          "prod_makes",
        ]
        users = [
          "prod_sorts",
        ]
        tags = {
          "Name"               = "prod_sorts"
          "management:area"    = "cost"
          "management:product" = "makes"
          "management:type"    = "product"
        }
      }
    }
  }
}

module "prod_sorts_aws" {
  source = "../../../modules/aws"

  name   = "prod_sorts"
  policy = local.prod_sorts.policies.aws

  extra_assume_role_policies = [
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
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

module "prod_sorts_keys" {
  source   = "../../../modules/key"
  for_each = local.prod_sorts.keys

  name   = each.key
  admins = each.value.admins
  users  = each.value.users
  tags   = each.value.tags
}

module "prod_sorts_publish_credentials" {
  source = "../../../modules/publish_credentials"

  providers = {
    gitlab = gitlab.product
  }

  key_1     = module.prod_sorts_aws.keys.1
  key_2     = module.prod_sorts_aws.keys.2
  prefix    = "PROD_SORTS"
  protected = true
}

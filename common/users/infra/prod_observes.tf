locals {
  # Redshift role Policy
  observes_redshift_cluster = {
    policies = {
      aws = {
        EtlDataAccess = [
          {
            Sid    = "MigrationBucketManagement"
            Effect = "Allow"
            Action = [
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
            Resource = [
              "arn:aws:s3:::observes.etl-data",
              "arn:aws:s3:::observes.etl-data/*",
            ]
          },
        ]
      }
    }
  }
  prod_observes = {
    policies = {
      aws = {
        ObservesGeneralAccess = [
          {
            Sid    = "terraformStateWrite"
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
            Sid    = "generalRead"
            Effect = "Allow"
            Action = [
              "batch:Describe*",
              "batch:List*",
              "cloudwatch:Describe*",
              "cloudwatch:Get*",
              "cloudwatch:List*",
              "dynamodb:BatchGet*",
              "dynamodb:Describe*",
              "dynamodb:Get*",
              "dynamodb:List*",
              "dynamodb:Query*",
              "dynamodb:Scan*",
              "ec2:Describe*",
              "ec2:Get*",
              "iam:Get*",
              "iam:List*",
              "kms:CreateAlias",
              "kms:CreateKey",
              "kms:Describe*",
              "kms:Get*",
              "kms:List*",
              "kms:TagResource",
              "kms:UntagResource",
              "kms:UpdateAlias",
              "logs:Describe*",
              "logs:Filter*",
              "logs:Get*",
              "logs:List*",
              "s3:Get*",
              "s3:List*",
              "tag:GetResources",
            ]
            Resource = ["*"]
          },
          {
            Sid    = "generalWrite"
            Effect = "Allow"
            Action = ["*"]
            Resource = [
              "arn:aws:s3:::integrates/continuous-repositories",
              "arn:aws:s3:::integrates/continuous-repositories/*",
              "arn:aws:s3:::integrates/continuous-data",
              "arn:aws:s3:::integrates/continuous-data/*",
              "arn:aws:s3:::fluidanalytics",
              "arn:aws:s3:::fluidanalytics/*",
              "arn:aws:s3:::fluidattacks-terraform-states-prod/observes-*",
              "arn:aws:s3:::observes*",
            ]
          },
        ]
        ObservesBatch = [
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
            "Condition" : { "StringEquals" : { "aws:RequestTag/management:product" : "observes" } }
          },
          {
            Sid    = "batchCancel"
            Effect = "Allow"
            Action = [
              "batch:CancelJob",
              "batch:TerminateJob",
            ]
            Resource = [
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job/*",
            ]
            "Condition" : { "StringEquals" : { "aws:ResourceTag/management:product" : "observes" } }
          },
          {
            Sid    = "batchSubmit"
            Effect = "Allow"
            Action = [
              "batch:SubmitJob",
            ]
            Resource = [
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job-definition/*",
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.main.account_id}:job-queue/*",
            ]
            "Condition" : { "StringEquals" : { "aws:RequestTag/management:product" : "observes" } }
          },
        ]
        ObservesRedshift = [
          {
            Sid    = "redshiftManager"
            Effect = "Allow"
            Action = [
              "redshift:*",
              "redshift-data:*",
              "redshift-serverless:*",
              "sqlworkbench:*",
            ]
            Resource = [
              "*",
            ]
          },
        ]
        ObservesKinesis = [
          {
            Sid    = "KinesisInfraManagement"
            Effect = "Allow"
            Action = [
              "kinesis:AddTagsToStream",
              "kinesis:CreateStream",
              "kinesis:DeleteStream",
              "kinesis:DecreaseStreamRetentionPeriod",
              "kinesis:DeregisterStreamConsumer",
              "kinesis:DisableEnhancedMonitoring",
              "kinesis:EnableEnhancedMonitoring",
              "kinesis:GetRecords",
              "kinesis:GetShardIterator",
              "kinesis:IncreaseStreamRetentionPeriod",
              "kinesis:MergeShards",
              "kinesis:RegisterStreamConsumer",
              "kinesis:RemoveTagsFromStream",
              "kinesis:SplitShard",
              "kinesis:StartStreamEncryption",
              "kinesis:StopStreamEncryption",
              "kinesis:SubscribeToShard",
              "kinesis:UpdateShardCount",
              "kinesis:UpdateStreamMode",
            ]
            Resource = [
              "arn:aws:kinesis:${var.region}:${data.aws_caller_identity.main.account_id}:stream/observes-mirror"
            ]
          },
          {
            Sid    = "KinesisInfraRead"
            Effect = "Allow"
            Action = [
              "kinesis:Describe*",
              "kinesis:List*",
            ]
            Resource = [
              "arn:aws:kinesis:${var.region}:${data.aws_caller_identity.main.account_id}:stream/observes-mirror"
            ]
          },
        ]
        ObservesSecGroups = [
          {
            Sid    = "manageObservesSecGroups"
            Effect = "Allow"
            Action = [
              "ec2:CreateSecurityGroup",
              "ec2:DeleteSecurityGroup",
              "ec2:AuthorizeSecurityGroupEgress",
              "ec2:AuthorizeSecurityGroupIngress",
              "ec2:RevokeSecurityGroupEgress",
              "ec2:RevokeSecurityGroupIngress",
              "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
              "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
              "ec2:CreateTags",
              "ec2:DeleteTags",
              "ec2:DescribeTags",
            ]
            Resource = ["*"]
          },
        ]
      }
    }

    keys = {
      prod_observes = {
        admins = [
          "prod_common",
        ]
        read_users = []
        users = [
          "prod_observes",
        ]
        tags = {
          "Name"               = "prod_observes"
          "management:area"    = "cost"
          "management:product" = "observes"
          "management:type"    = "product"
        }
      }
    }
  }
}

module "prod_observes" {
  source = "./modules/aws"

  name     = "prod_observes"
  policies = local.prod_observes.policies.aws
  assume_role_policy = [
    {
      Sid    = "graphanaUserAccess",
      Effect = "Allow",
      Principal = {
        "AWS" = [
          aws_iam_user.graphana_user.arn
        ]
      },
      Action = "sts:AssumeRole",
    },
  ]
  tags = {
    "Name"               = "prod_observes"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}

module "observes_redshift_aws" {
  source = "./modules/aws"

  name     = "observes_redshift_cluster"
  policies = local.observes_redshift_cluster.policies.aws
  assume_role_policy = [
    {
      Sid    = "RedshiftAccess",
      Effect = "Allow",
      Principal = {
        Service = "redshift.amazonaws.com"
      },
      Action = "sts:AssumeRole"
    }
  ]
  tags = {
    "Name"               = "observes_redshift_cluster"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}

module "prod_observes_keys" {
  source   = "./modules/key"
  for_each = local.prod_observes.keys

  name       = each.key
  admins     = each.value.admins
  read_users = each.value.read_users
  users      = each.value.users
  tags       = each.value.tags
}

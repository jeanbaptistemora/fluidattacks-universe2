locals {
  # Redshift role Policy
  observes_redshift = {
    policies = {
      aws = [
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
  prod_observes = {
    policies = {
      aws = [
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
        {
          # required to rename tags
          Sid    = "redshiftTags"
          Effect = "Allow"
          Action = [
            "redshift:CreateTags",
            "redshift:DeleteTags",
            "redshift:DescribeTags",
          ]
          Resource = [
            "arn:aws:redshift:${var.region}:${data.aws_caller_identity.main.account_id}:subnetgroup:observes",
          ]
        },
        {
          Sid    = "redshiftWrite"
          Effect = "Allow"
          Action = [
            "redshift:*",
          ]
          Resource = [
            "arn:aws:redshift:${var.region}:${data.aws_caller_identity.main.account_id}:cluster:observes",
          ]
        },
        {
          Sid    = "redshiftClustersRead"
          Effect = "Allow"
          Action = [
            "redshift:DescribeClusterSubnetGroups",
            "redshift:DescribeEvents",
            "redshift:DescribeClusters",
            "redshift:DescribeClusterSnapshots",
            "redshift:DescribeUsageLimits",
            "redshift:DescribeSnapshotSchedules",
          ]
          Resource = [
            "arn:aws:redshift:${var.region}:${data.aws_caller_identity.main.account_id}:subnetgroup:*",
            "arn:aws:redshift:${var.region}:${data.aws_caller_identity.main.account_id}:event:*",
            "arn:aws:redshift:${var.region}:${data.aws_caller_identity.main.account_id}:cluster:*",
            "arn:aws:redshift:${var.region}:${data.aws_caller_identity.main.account_id}:snapshot:*/*",
            "arn:aws:redshift:${var.region}:${data.aws_caller_identity.main.account_id}:snapshotschedule:*",
            "arn:aws:redshift:${var.region}:${data.aws_caller_identity.main.account_id}:usagelimit:*",
          ]
        },
        {
          # required for some redshift front views
          Sid    = "redshiftGeneralRead"
          Effect = "Allow"
          Action = [
            "redshift:DescribeReservedNodes",
            "redshift:DescribeClusterDbRevisions",
            "redshift:DescribeScheduledActions",
            "redshift:DescribeHsmConfigurations",
            "redshift:DescribePartners",
          ]
          Resource = [
            "*",
          ]
        },
        {
          Sid    = "redshiftReadSecrets"
          Effect = "Allow"
          Action = [
            "redshift:GetClusterCredentials",
          ]
          Resource = [
            "arn:aws:redshift:${var.region}:${data.aws_caller_identity.main.account_id}:dbname:observes/*",
            "arn:aws:redshift:${var.region}:${data.aws_caller_identity.main.account_id}:dbuser:observes/*",
          ]
        },
        {
          Sid    = "redshiftSavedQueries"
          Effect = "Allow"
          Action = [
            "redshift:CreateSavedQuery",
            "redshift:ModifySavedQuery",
            "redshift:DeleteSavedQueries",
            "redshift:DescribeSavedQueries",
            "redshift:ListSavedQueries",
          ]
          Resource = ["*"]
        },
        {
          Sid    = "redshiftExecuteSqlOnConsole"
          Effect = "Allow"
          Action = [
            "redshift-data:BatchExecuteStatement",
            "redshift-data:DescribeTable",
            "redshift-data:ExecuteStatement",
            "redshift-data:ListDatabases",
            "redshift-data:ListSchemas",
            "redshift-data:ListTables",
          ]
          Resource = [
            "arn:aws:redshift:${var.region}:${data.aws_caller_identity.main.account_id}:cluster:observes",
          ]
        },
        {
          Sid    = "redshiftExecuteSqlOnConsole2"
          Effect = "Allow"
          Action = [
            "redshift-data:CancelStatement",
            "redshift-data:DescribeStatement",
            "redshift-data:GetStatementResult",
            "redshift-data:ListStatements",
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
          Sid    = "manageObservesIAM"
          Effect = "Allow"
          Action = [
            "iam:AttachRolePolicy",
            "iam:CreatePolicy",
            "iam:CreatePolicyVersion",
            "iam:CreateRole",
            "iam:DeletePolicy",
            "iam:DeletePolicyVersion",
            "iam:DeleteRole",
            "iam:DeleteRolePolicy",
            "iam:DetachRolePolicy",
            "iam:PassRole",
            "iam:PutRolePolicy",
            "iam:TagRole",
            "iam:UpdateAssumeRolePolicy",
            "iam:UntagRole",
          ]
          Resource = [
            "arn:aws:iam::${data.aws_caller_identity.main.account_id}:policy/analytics",
            "arn:aws:iam::${data.aws_caller_identity.main.account_id}:role/analytics",
            "arn:aws:iam::${data.aws_caller_identity.main.account_id}:user/analytics/analytics",
            "arn:aws:iam::${data.aws_caller_identity.main.account_id}:role/observes*",
            "arn:aws:iam::${data.aws_caller_identity.main.account_id}:policy/observes*",
            "arn:aws:iam::${data.aws_caller_identity.main.account_id}:role/redshift*",
            "arn:aws:iam::${data.aws_caller_identity.main.account_id}:policy/redshift*",
          ]
        },
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

module "prod_observes_aws" {
  source = "./modules/aws"

  name   = "prod_observes"
  policy = local.prod_observes.policies.aws
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

  name   = "observes_redshift"
  policy = local.observes_redshift.policies.aws
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
    "Name"               = "observes_redshift"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}

resource "aws_iam_role_policy_attachment" "apply_kinessis_infra_manager" {
  role       = "prod_observes"
  policy_arn = aws_iam_policy.observes_kinesis_infra_management.arn
}

resource "aws_iam_role_policy_attachment" "apply_kinesis_infra_read" {
  role       = "prod_observes"
  policy_arn = aws_iam_policy.observes_kinesis_infra_read.arn
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

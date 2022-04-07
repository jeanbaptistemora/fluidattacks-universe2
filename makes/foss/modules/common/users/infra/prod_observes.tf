locals {
  prod_observes = {
    policies = {
      aws = {
        Version = "2012-10-17"
        Statement = [
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
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/analytics",
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/observes*",
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/analytics",
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/observes-*",
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/analytics/analytics",
              "arn:aws:s3:::continuous-repositories",
              "arn:aws:s3:::continuous-repositories/*",
              "arn:aws:s3:::continuous-data",
              "arn:aws:s3:::continuous-data/*",
              "arn:aws:s3:::fluidanalytics",
              "arn:aws:s3:::fluidanalytics/*",
              "arn:aws:s3:::fluidattacks-terraform-states-prod/observes-*",
              "arn:aws:s3:::observes*",
            ]
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
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job/*",
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-definition/*",
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/dedicated*",
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/observes*",
              "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/spot*",
            ]
          },
          {
            Sid    = "redshiftWrite"
            Effect = "Allow"
            Action = [
              "redshift:*",
              "redshift-data:*",
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
              "iam:DeleteRole",
              "iam:DeleteRolePolicy",
              "iam:DetachRolePolicy",
              "iam:PassRole",
              "iam:PutRolePolicy",
              "iam:TagRole",
              "iam:UpdateAssumeRolePolicy",
            ]
            Resource = [
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/observes*",
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/observes*",
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/redshift*",
              "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/redshift*",
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
    }

    keys = {
      prod_observes = {
        admins = [
          "prod_makes",
        ]
        users = [
          "prod_observes",
        ]
        tags = {
          "Name"               = "prod_observes"
          "management:area"    = "cost"
          "management:product" = "makes"
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

  tags = {
    "Name"               = "prod_observes"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

module "prod_observes_keys" {
  source   = "./modules/key"
  for_each = local.prod_observes.keys

  name   = each.key
  admins = each.value.admins
  users  = each.value.users
  tags   = each.value.tags
}

module "prod_observes_publish_credentials" {
  source = "./modules/publish_credentials"

  providers = {
    gitlab = gitlab.product
  }

  key_1     = module.prod_observes_aws.keys.1
  key_2     = module.prod_observes_aws.keys.2
  prefix    = "PROD_OBSERVES"
  protected = true
}

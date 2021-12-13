locals {
  aws = {
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "iamRead"
        Effect = "Allow"
        Action = [
          "iam:List*",
          "iam:Get*",
          "iam:Create*",
        ]
        Resource = ["*"]
      },
      {
        Sid    = "iamWrite"
        Effect = "Allow"
        Action = ["*"]
        Resource = [
          "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/aws-service-role/dynamodb.application-autoscaling.amazonaws.com/AWSServiceRoleForApplicationAutoScaling_DynamoDBTable",
          "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/integrates*",
          "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/integrates*",
        ]
      },
      {
        Sid    = "elasticacheRead"
        Effect = "Allow"
        Action = [
          "elasticache:Describe*",
          "elasticache:List*",
          "elasticache:CreateReplicationGroup",
          "elasticache:CreateCacheSecurityGroup",
          "elasticache:CreateCacheSubnetGroup",
          "elasticache:AddTagsToResource",
        ]
        Resource = ["*"]
      },
      {
        Sid    = "elasticacheWrite"
        Effect = "Allow"
        Action = ["*"]
        Resource = [
          "arn:aws:elasticache:${var.region}:${data.aws_caller_identity.current.account_id}:cluster:integrates-*",
          "arn:aws:elasticache:${var.region}:${data.aws_caller_identity.current.account_id}:replicationgroup:integrates-*",
          "arn:aws:elasticache:${var.region}:${data.aws_caller_identity.current.account_id}:subnetgroup:integrates-*",
        ]
      },
      {
        Sid    = "s3Read"
        Effect = "Allow"
        Action = [
          "s3:Get*",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::continuous-data",
          "arn:aws:s3:::continuous-data/*",
        ]
      },
      {
        Sid    = "s3Write"
        Effect = "Allow"
        Action = ["*"]
        Resource = [
          "arn:aws:s3:::fluidattacks-terraform-states-prod/integrates*",
          "arn:aws:s3:::fluidintegrates*/*",
          "arn:aws:s3:::fluidintegrates*",
          "arn:aws:s3:::integrates*/*",
          "arn:aws:s3:::integrates*",
        ]
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
        Action = ["*"]
        Resource = [
          "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-definition/*",
          "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/skims*",
          "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/spot*",
          "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/dedicated_soon",
          "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/dedicated_later",
        ]
      },
      {
        Sid    = "logsRead"
        Effect = "Allow"
        Action = [
          "logs:Describe*",
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
          "arn:aws:logs:us-east-1:${data.aws_caller_identity.current.account_id}:log-group:FLUID*",
        ]
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
        Sid    = "ec2Read"
        Effect = "Allow"
        Action = [
          "ec2:Describe*",
          "ec2:Get*",
        ]
        Resource = ["*"]
      },
      {
        Sid    = "ec2Write"
        Effect = "Allow"
        Action = [
          "ec2:RevokeSecurityGroupEgress",
          "ec2:RevokeSecurityGroupIngress",
          "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
          "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
          "ec2:ApplySecurityGroupsToClientVpnTargetNetwork",
          "ec2:AuthorizeSecurityGroupEgress",
          "ec2:AuthorizeSecurityGroupIngress",
          "ec2:CreateSecurityGroup",
          "ec2:DeleteSecurityGroup",
        ]
        Resource = ["*"]
      },
      {
        Sid    = "eksRead"
        Effect = "Allow"
        Action = [
          "eks:Describe*",
          "eks:Get*",
        ]
        Resource = ["*"]
      },
      {
        Sid    = "eksWrite"
        Effect = "Allow"
        Action = ["*"]
        Resource = [
          "arn:aws:eks:${var.region}:${data.aws_caller_identity.current.account_id}:cluster/integrates-*"
        ]
      },
      {
        Sid      = "dynamoWrite"
        Effect   = "Allow"
        Action   = ["dynamodb:*"]
        Resource = ["*"]
      },
      {
        Sid    = "backupWrite"
        Effect = "Allow"
        Action = [
          "backup:*",
          "backup-storage:*",
        ]
        Resource = ["*"]
      },
    ]
  }
  cloudflare = {
    accountZone = {
      effect = "allow"
      permission_groups = [
        data.cloudflare_api_token_permission_groups.all.permissions["Zone Read"],
        data.cloudflare_api_token_permission_groups.all.permissions["Page Rules Write"],
        data.cloudflare_api_token_permission_groups.all.permissions["Firewall Services Write"],
        data.cloudflare_api_token_permission_groups.all.permissions["DNS Write"],
        data.cloudflare_api_token_permission_groups.all.permissions["Cache Purge"],
      ]
      resources = {
        "com.cloudflare.api.account.zone.*" = "*"
      }
    }
  }
}

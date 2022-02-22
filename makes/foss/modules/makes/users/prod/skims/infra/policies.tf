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
          "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-definition/*",
          "arn:aws:batch:us-east-1:${data.aws_caller_identity.current.account_id}:job-queue/skims*",
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
          "arn:aws:logs:us-east-1:${data.aws_caller_identity.current.account_id}:log-group:skims",
          "arn:aws:logs:us-east-1:${data.aws_caller_identity.current.account_id}:log-group:skims:log-stream:*",
        ]
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
          "ec2:ApplySecurityGroupsToClientVpnTargetNetwork",
          "ec2:AuthorizeSecurityGroupEgress",
          "ec2:AuthorizeSecurityGroupIngress",
          "ec2:Create*",
          "ec2:DeleteNetworkInterface",
          "ec2:DeleteSecurityGroup",
          "ec2:DeleteSubnet",
          "ec2:DeleteTags",
          "ec2:ModifySubnetAttribute",
          "ec2:RevokeSecurityGroupEgress",
          "ec2:RevokeSecurityGroupIngress",
          "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
          "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
        ]
        Resource = ["*"]
      },
      {
        Sid    = "s3Read"
        Effect = "Allow"
        Action = [
          "s3:ListBucket",
        ]
        Resource = [
          "arn:aws:s3:::fluidattacks.com",
        ]
      },
      {
        Sid    = "s3Write"
        Effect = "Allow"
        Action = ["*"]
        Resource = [
          "arn:aws:s3:::fluidattacks.com/resources/doc/skims/*",
          "arn:aws:s3:::fluidattacks-terraform-states-prod/skims*",
          "arn:aws:s3:::skims*",
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
        Sid    = "dynamoReadJobs"
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:Query",
          "dynamodb:DeleteItem",
        ]
        Resource = [
          "arn:aws:dynamodb:us-east-1:205810638802:table/fi_async_processing",
        ]
      },
    ]
  }
}

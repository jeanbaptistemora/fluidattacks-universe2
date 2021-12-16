locals {
  aws = {
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "allWrite"
        Effect = "Allow"
        Action = [
          "access-analyzer:*",
          "acm:*",
          "autoscaling:*",
          "aws-portal:*",
          "backup:*",
          "batch:*",
          "budgets:*",
          "ce:*",
          "cloudwatch:*",
          "compute-optimizer:*",
          "cur:*",
          "dynamodb:*",
          "ec2:*",
          "ecr:*",
          "ecs:*",
          "eks:*",
          "elasticache:*",
          "elasticloadbalancing:*",
          "events:*",
          "iam:*",
          "kms:*",
          "lambda:*",
          "logs:*",
          "pricing:*",
          "rds:*",
          "route53:*",
          "s3:*",
          "savingsplans:*",
          "secretsmanager:*",
          "sns:*",
          "sqs:*",
          "ssm:*",
          "sts:*",
          "tag:*",
        ]
        Resource = ["*"]
      },
    ]
  }
}

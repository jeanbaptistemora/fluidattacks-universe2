resource "aws_iam_policy" "CloudFormation_Lambda" {
  name        = "CloudFormation_Lambda"
  path        = "/"
  description = "Policy for cloudformation-lambda"

  policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "lambda:CreateFunction",
                "cloudformation:ListStacks",
                "lambda:UpdateEventSourceMapping",
                "lambda:ListFunctions",
                "lambda:GetEventSourceMapping",
                "lambda:UpdateFunctionConfiguration",
                "s3:CreateBucket",
                "s3:ListBucket",
                "lambda:GetAccountSettings",
                "s3:GetBucketVersioning",
                "lambda:CreateEventSourceMapping",
                "cloudformation:CreateChangeSet",
                "s3:ListObjects",
                "cloudformation:CreateStack",
                "lambda:ListEventSourceMappings",
                "cloudformation:DescribeAccountLimits",
                "cloudformation:UpdateStack",
                "lambda:DeleteEventSourceMapping",
                "cloudformation:DescribeChangeSet",
                "s3:DeleteBucket",
                "cloudformation:ExecuteChangeSet",
                "cloudformation:ValidateTemplate"
            ],
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor1",
            "Effect": "Allow",
            "Action": [
                "iam:GetRole",
                "s3:PutObject",
                "s3:GetObject",
                "apigateway:POST",
                "s3:DeleteObject",
                "iam:GetRolePolicy",
                "cloudformation:DescribeStacks"
            ],
            "Resource": [
                "arn:aws:apigateway:*::*",
                "arn:aws:cloudformation:*:*:stack/*/*",
                "arn:aws:iam::*:role/*",
                "arn:aws:s3:::*/*"
            ]
        },
        {
            "Sid": "VisualEditor2",
            "Effect": "Allow",
            "Action": [
                "cloudformation:DescribeStackEvents",
                "s3:PutAccelerateConfiguration",
                "iam:CreateRole",
                "apigateway:GET"
            ],
            "Resource": [
                "arn:aws:s3:::*",
                "arn:aws:iam::*:role/*",
                "arn:aws:cloudformation:*:*:stack/*/*",
                "arn:aws:apigateway:*::*"
            ]
        },
        {
            "Sid": "VisualEditor3",
            "Effect": "Allow",
            "Action": [
                "apigateway:*",
                "iam:PutUserPolicy",
                "cloudformation:DescribeStackResources",
                "cloudformation:DescribeStackResource",
                "iam:PutRolePolicy"
            ],
            "Resource": [
                "arn:aws:iam::*:user/*",
                "arn:aws:iam::*:role/*",
                "arn:aws:apigateway:*::*",
                "arn:aws:cloudformation:*:*:stack/*/*"
            ]
        },
        {
            "Sid": "VisualEditor4",
            "Effect": "Allow",
            "Action": "iam:PassRole",
            "Resource": "arn:aws:iam::*:role/*"
        },
        {
            "Sid": "VisualEditor5",
            "Effect": "Allow",
            "Action": "lambda:*",
            "Resource": "arn:aws:lambda:*:*:function:*"
        }
    ]
}
EOF
}

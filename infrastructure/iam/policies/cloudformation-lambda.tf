data "aws_iam_policy_document" "cflambda-policy" {
  statement {
    sid = "VisualEditor0"
    effect = "Allow"
    actions = [
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
      "cloudformation:ValidateTemplate",
    ]

    resources = [
      "*",
    ]
  }

  statement {
    sid = "VisualEditor1"
    effect = "Allow"
    actions = [
      "iam:GetRole",
      "s3:PutObject",
      "s3:GetObject",
      "apigateway:POST",
      "s3:DeleteObject",
      "iam:GetRolePolicy",
      "cloudformation:DescribeStacks",
    ]

    resources = [
      "arn:aws:apigateway:*::*",
      "arn:aws:cloudformation:*:*:stack/*/*",
      "arn:aws:iam::*:role/*",
      "arn:aws:s3:::*/*",
    ]
  }

  statement {
    sid = "VisualEditor2"
    effect = "Allow"
    actions = [
      "cloudformation:DescribeStackEvents",
      "s3:PutAccelerateConfiguration",
      "iam:CreateRole",
      "apigateway:GET",
    ]

    resources = [
      "arn:aws:s3:::*",
      "arn:aws:iam::*:role/*",
      "arn:aws:cloudformation:*:*:stack/*/*",
      "arn:aws:apigateway:*::*",
    ]
  }

  statement {
    sid = "VisualEditor3"
    effect = "Allow"
    actions = [
      "apigateway:*",
      "iam:PutUserPolicy",
      "cloudformation:DescribeStackResources",
      "cloudformation:DescribeStackResource",
      "iam:PutRolePolicy",
    ]

    resources = [
      "arn:aws:iam::*:user/*",
      "arn:aws:iam::*:role/*",
      "arn:aws:apigateway:*::*",
      "arn:aws:cloudformation:*:*:stack/*/*",
    ]
  }

  statement {
    sid = "VisualEditor4"
    effect = "Allow"
    actions = [
      "iam:PassRole"
    ]

    resources = [
      "arn:aws:iam::*:role/*"
    ]
  }

  statement {
    sid = "VisualEditor5"
    effect = "Allow"
    actions = [
      "lambda:*"
    ]

    resources = [
      "arn:aws:lambda:*:*:function:*"
    ]
  }

  }


resource "aws_iam_policy" "CloudFormation_Lambda" {
  name        = "CloudFormation_Lambda"
  path        = "/"
  description = "Policy for cloudformation-lambda"
  policy = data.aws_iam_policy_document.cflambda-policy.json
}

data "aws_iam_policy_document" "aws-python-fluidcounts-policy" {
  statement {
    effect = "Allow"
    actions = [
      "sts:AssumeRole"
    ]
    principals {
      type = "Service"
      identifiers = [
        "lambda.amazonaws.com"
      ]
    }
  }
}

data "aws_iam_policy_document" "awspython-inline-policy" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
    ]
    resources = [
      "arn:aws:logs:us-east-1:205810638802:log-group:/aws/lambda/aws-python-fluidcounts-dev-countCode:*"
    ]
  }

  statement {
    effect = "Allow"
    actions = [
      "logs:PutLogEvents",
    ]
    resources = [
      "arn:aws:logs:us-east-1:205810638802:log-group:/aws/lambda/aws-python-fluidcounts-dev-countCode:*:*"
    ]
  }
}

resource "aws_iam_role" "awspython" {
  name = "aws-python-fluidcounts-dev-us-east-1-lambdaRole"

  assume_role_policy = "${data.aws_iam_policy_document.aws-python-fluidcounts-policy.json}"
}

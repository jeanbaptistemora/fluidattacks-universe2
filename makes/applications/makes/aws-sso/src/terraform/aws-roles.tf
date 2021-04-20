# Airs

resource "aws_iam_role" "airs_dev" {
  name                 = "airs_dev"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "airs_dev"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_role_policy_attachment" "airs_dev" {
  role       = aws_iam_role.airs_dev.name
  policy_arn = "arn:aws:iam::205810638802:policy/user-provision/web-dev-policy"
}

resource "aws_iam_role" "airs_prod" {
  name                 = "airs_prod"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "airs_prod"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_role_policy_attachment" "airs_prod" {
  role       = aws_iam_role.airs_prod.name
  policy_arn = "arn:aws:iam::205810638802:policy/user-provision/web-prod-policy"
}


# Docs

resource "aws_iam_role" "docs_dev" {
  name                 = "docs_dev"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "docs_dev"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_role_policy_attachment" "docs_dev" {
  role       = aws_iam_role.docs_dev.name
  policy_arn = "arn:aws:iam::205810638802:policy/user-provision/docs_dev"
}

resource "aws_iam_role" "docs_prod" {
  name                 = "docs_prod"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "docs_prod"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_role_policy_attachment" "docs_prod" {
  role       = aws_iam_role.docs_prod.name
  policy_arn = "arn:aws:iam::205810638802:policy/user-provision/docs_prod"
}


# Finance

data "aws_iam_policy_document" "erp-finance-policy-data" {
  statement {
    sid    = "AllowStartAndStopInstance"
    effect = "Allow"
    actions = [
      "ec2:StartInstances",
      "ec2:StopInstances"
    ]
    resources = [
      "arn:aws:ec2:us-east-1:${data.aws_caller_identity.current.account_id}:instance/i-0ba149836e9bb8e7c"
    ]
  }
}

resource "aws_iam_policy" "erp-finance-policy" {
  name        = "erp-finance"
  path        = "/"
  description = "Policy for turning on and off the erp machine"

  policy = data.aws_iam_policy_document.erp-finance-policy-data.json
}

resource "aws_iam_role" "finance-role" {
  name               = "finance"
  assume_role_policy = data.aws_iam_policy_document.okta-assume-role-policy-data.json

  tags = {
    "Name"               = "finance"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_role_policy_attachment" "finance-role-erp" {
  role       = aws_iam_role.finance-role.name
  policy_arn = aws_iam_policy.erp-finance-policy.arn
}

resource "aws_iam_role_policy_attachment" "finance-role-read-ec2" {
  role       = aws_iam_role.finance-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
}


# Helpdesk

data "aws_iam_policy_document" "helpdesk-policy-data" {
  statement {
    effect = "Allow"
    actions = [
      "ec2:Describe*Instance*",
      "ec2:StartInstances",
      "ec2:StopInstances",
      "ec2:ApplySecurityGroupsToClientVpnTargetNetwork",
      "ec2:DescribeSecurityGroupReferences",
      "ec2:DescribeSecurityGroups",
      "ec2:DescribeStaleSecurityGroups",
      "ec2:UpdateSecurityGroupRuleDescriptionsEgress",
      "ec2:UpdateSecurityGroupRuleDescriptionsIngress",
    ]
    resources = ["*"]
  }
}

resource "aws_iam_policy" "helpdesk-policy" {
  name        = "helpdesk"
  path        = "/"
  description = "Policy for heldesk role"

  policy = data.aws_iam_policy_document.helpdesk-policy-data.json
}

resource "aws_iam_role" "helpdesk-role" {
  name               = "helpdesk"
  assume_role_policy = data.aws_iam_policy_document.okta-assume-role-policy-data.json

  tags = {
    "Name"               = "helpdesk"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_role_policy_attachment" "helpdesk-role" {
  role       = aws_iam_role.helpdesk-role.name
  policy_arn = aws_iam_policy.helpdesk-policy.arn
}

resource "aws_iam_role_policy_attachment" "helpdesk-policy" {
  role       = aws_iam_role.helpdesk-role.name
  policy_arn = aws_iam_policy.helpdesk-policy.arn
}


# Makes

resource "aws_iam_role" "makes_prod" {
  name                 = "makes_prod"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "makes_prod"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_role_policy_attachment" "makes_prod_ec2" {
  role       = aws_iam_role.makes_prod.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}

resource "aws_iam_role_policy_attachment" "makes_prod_code_commit" {
  role       = aws_iam_role.makes_prod.name
  policy_arn = "arn:aws:iam::aws:policy/AWSCodeCommitFullAccess"
}

resource "aws_iam_role_policy_attachment" "makes_prod_lambda" {
  role       = aws_iam_role.makes_prod.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaFullAccess"
}

resource "aws_iam_role_policy_attachment" "makes_prod_iam" {
  role       = aws_iam_role.makes_prod.name
  policy_arn = "arn:aws:iam::aws:policy/IAMFullAccess"
}

resource "aws_iam_role_policy_attachment" "makes_prod_simple_worflow" {
  role       = aws_iam_role.makes_prod.name
  policy_arn = "arn:aws:iam::aws:policy/SimpleWorkflowFullAccess"
}

resource "aws_iam_role_policy_attachment" "makes_prod_s3" {
  role       = aws_iam_role.makes_prod.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "makes_prod_sns" {
  role       = aws_iam_role.makes_prod.name
  policy_arn = "arn:aws:iam::aws:policy/AWSCloudTrailFullAccess"
}

resource "aws_iam_role_policy_attachment" "makes_prod_admin" {
  role       = aws_iam_role.makes_prod.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_iam_role_policy_attachment" "makes_prod_route_53" {
  role       = aws_iam_role.makes_prod.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonRoute53FullAccess"
}

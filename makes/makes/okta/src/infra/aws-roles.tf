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
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/web-dev-policy"
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
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/web-prod-policy"
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
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/docs_dev"
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
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/docs_prod"
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

resource "aws_iam_role_policy_attachment" "makes_prod" {
  role       = aws_iam_role.makes_prod.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/serves-prod-policy"
}

# Observes

resource "aws_iam_role" "observes_dev" {
  name                 = "observes_dev"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "observes_dev"
    "management:type"    = "production"
    "management:product" = "observes"
  }
}

resource "aws_iam_role_policy_attachment" "observes_dev" {
  role       = aws_iam_role.observes_dev.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/observes-dev-policy"
}

resource "aws_iam_role" "observes_prod" {
  name                 = "observes_prod"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "observes_prod"
    "management:type"    = "production"
    "management:product" = "observes"
  }
}

resource "aws_iam_role_policy_attachment" "observes_prod" {
  role       = aws_iam_role.observes_prod.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/observes-prod-policy"
}

# Skims

resource "aws_iam_role" "skims_dev" {
  name                 = "skims_dev"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "skims_dev"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_role_policy_attachment" "skims_dev" {
  role       = aws_iam_role.skims_dev.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user_provision/skims_dev_policy"
}

resource "aws_iam_role" "skims_prod" {
  name                 = "skims_prod"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "skims_prod"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_role_policy_attachment" "skims_prod" {
  role       = aws_iam_role.skims_prod.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user_provision/skims_prod_policy"
}

# Sorts

data "aws_iam_policy_document" "sorts_assume_role_policy" {
  statement {
    sid    = "OktaSAMLAccess"
    effect = "Allow"
    actions = [
      "sts:AssumeRoleWithSAML"
    ]

    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.current.account_id}:saml-provider/okta-saml-provider"]
    }
    condition {
      test     = "StringEquals"
      variable = "SAML:aud"
      values = [
        "https://signin.aws.amazon.com/saml"
      ]
    }
  }

  statement {
    sid    = "SageMakerAssumeRolePolicy"
    effect = "Allow"
    actions = [
      "sts:AssumeRole",
    ]

    principals {
      type = "Service"
      identifiers = [
        "sagemaker.amazonaws.com"
      ]
    }
  }
}

resource "aws_iam_role" "sorts_prod" {
  name                 = "sorts_prod"
  assume_role_policy   = data.aws_iam_policy_document.sorts_assume_role_policy.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "sorts_prod"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_role_policy_attachment" "sorts_prod" {
  role       = aws_iam_role.sorts_prod.name
  policy_arn = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user_provision/sorts_prod_policy"
}

data "aws_iam_policy_document" "web-prod-policy-data" {

  # S3 web prod and ephemeral buckets
  statement {
    effect  = "Allow"
    actions = ["s3:*"]
    resources = [
      "arn:aws:s3:::web.fluidattacks.com/*",
      "arn:aws:s3:::web.fluidattacks.com",
      "arn:aws:s3:::web.eph.fluidattacks.com/*",
      "arn:aws:s3:::web.eph.fluidattacks.com",
    ]
  }

  # S3 state files
  statement {
    effect = "Allow"
    actions = [
      "s3:PutObject",
      "s3:ListBucket",
      "s3:GetObject"
    ]
    resources = [
      "arn:aws:s3:::fluidattacks-terraform-states-*",
      "arn:aws:s3:::fluidattacks-terraform-states-prod/web-secret-management.tfstate",
      "arn:aws:s3:::fluidattacks-terraform-states-*/user-provision-web-*.tfstate",
    ]
  }

  # IAM full permissions over owned users, roles and policies
  statement {
    effect  = "Allow"
    actions = [
      "iam:*"
    ]
    resources = [
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/web-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:user/web-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/web-*",
      "arn:aws:iam::${data.aws_caller_identity.current.account_id}:policy/user-provision/web-*",
    ]
  }

  # Cloudfront write distribuions and OAI
  statement {
    effect  = "Allow"
    actions = [
      "cloudfront:CreateDistribution",
      "cloudfront:UpdateDistribution",
      "cloudfront:TagResource",
      "cloudfront:GetDistribution",
      "cloudfront:ListTagsForResource",
      "cloudfront:CreateCloudFrontOriginAccessIdentity",
      "cloudfront:GetCloudFrontOriginAccessIdentity",
      "cloudfront:DeleteCloudFrontOriginAccessIdentity"
    ]
    resources = [
      "*"
    ]
  }

  # ACM create and read certificate
  statement {
    effect  = "Allow"
    actions = [
      "acm:RequestCertificate",
      "acm:DescribeCertificate",
      "acm:ListTagsForCertificate",
    ]
    resources = [
      "*",
    ]
  }

  # Route 53 basic read
  statement {
    effect  = "Allow"
    actions = [
      "route53:ListHostedZones",
      "route53:GetHostedZone",
      "route53:GetChange"
    ]
    resources = [
      "*",
    ]
  }

  # Route 53 read/write over fluidattacks hosted zone
  statement {
    effect  = "Allow"
    actions = [
      "route53:ListTagsForResource",
      "route53:ChangeResourceRecordSets",
      "route53:ListResourceRecordSets"
    ]
    resources = [
      "arn:aws:route53:::hostedzone/${data.aws_route53_zone.fluidattacks.zone_id}",
    ]
  }

  # KMS create Keys
  statement {
    effect = "Allow"
    actions = [
      "kms:UntagResource",
      "kms:TagResource",
      "kms:List*",
      "kms:Get*",
      "kms:Describe*",
      "kms:CreateKey",
      "kms:CreateAlias",
      "kms:UpdateAlias"
    ]
    resources = [
      "*"
    ]
  }

  # KMS full permissions
  statement {
    effect  = "Allow"
    actions = [
      "kms:*"
    ]
    resources = [
      "arn:aws:kms:${var.region}:${data.aws_caller_identity.current.account_id}:alias/web-*"
    ]
  }
}

resource "aws_iam_policy" "web-prod-policy" {
  description = "web-prod policy"
  name        = "${var.user-name}-policy"
  path        = "/user-provision/"
  policy      = data.aws_iam_policy_document.web-prod-policy-data.json
}

resource "aws_iam_user_policy_attachment" "web-prod-attach-policy" {
  user       = var.user-name
  policy_arn = aws_iam_policy.web-prod-policy.arn
}

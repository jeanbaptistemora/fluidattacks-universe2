# Clouxter

resource "aws_iam_user" "clouxter_erika_bayona" {
  name = "erika.bayona"
  path = "/user-provision/"

  tags = {
    "Name"               = "erika.bayona"
    "Management:Area"    = "cost"
    "Management:Product" = "common"
    "Management:Type"    = "product"
  }
}

resource "aws_iam_user_policy_attachment" "clouxter_erika_bayona_password" {
  user       = aws_iam_user.clouxter_erika_bayona.name
  policy_arn = "arn:aws:iam::aws:policy/IAMUserChangePassword"
}

resource "aws_iam_user_policy_attachment" "clouxter_erika_bayona_billing" {
  user       = aws_iam_user.clouxter_erika_bayona.name
  policy_arn = "arn:aws:iam::aws:policy/AWSBillingReadOnlyAccess"
}

resource "aws_iam_user_policy_attachment" "clouxter_erika_bayona_cloudtrail" {
  user       = aws_iam_user.clouxter_erika_bayona.name
  policy_arn = "arn:aws:iam::aws:policy/AWSCloudTrailReadOnlyAccess"
}

# Snowflake
data "aws_iam_policy_document" "snowflake-read-policy-doc" {
  statement {
    sid    = "SnowflakeS3ReadAccess"
    effect = "Allow"

    actions = [
      "s3:GetBucketLocation",
      "s3:GetObject",
      "s3:GetObjectVersion",
      "s3:ListBucket",
    ]

    resources = [
      "arn:aws:s3:::observes.etl-data",
      "arn:aws:s3:::observes.etl-data/*",
    ]
  }
}
resource "aws_iam_policy" "snowflake-read-policy" {
  name        = "snowflake-read-policy"
  path        = "/"
  description = "Policy for snowflake s3 read access"
  policy      = data.aws_iam_policy_document.snowflake-read-policy-doc.json
}

resource "aws_iam_user" "snowflake-user" {
  name = "snowflake-user"
  path = "/user-provision/"

  tags = {
    "Name"               = "snowflake_prod"
    "Management:Area"    = "cost"
    "Management:Product" = "observes"
    "Management:Type"    = "product"
  }
}

resource "aws_iam_user_policy" "snowflake-user-policy" {
  name   = "snowflake-user-policy"
  user   = aws_iam_user.snowflake-user.name
  policy = aws_iam_policy.snowflake-read-policy.arn
}

resource "aws_iam_access_key" "snowflake-access-key" {
  user = aws_iam_user.snowflake-user.name
}

module "snowflake_publish_credentials" {
  source = "./modules/publish_credentials"

  providers = {
    gitlab = gitlab.universe
  }

  key_1     = aws_iam_access_key.snowflake-access-key
  key_2     = aws_iam_access_key.snowflake-access-key
  prefix    = "PROD_SNOWFLAKE"
  protected = true
}

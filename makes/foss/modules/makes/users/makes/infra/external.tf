# Clouxter

resource "aws_iam_user" "clouxter_erika_bayona" {
  name = "erika.bayona"
  path = "/user-provision/"

  tags = {
    "Name"               = "erika.bayona"
    "management:type"    = "production"
    "management:product" = "makes"
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


resource "aws_iam_user" "clouxter_michelle_hernandez" {
  name = "michelle.hernandez"
  path = "/user-provision/"

  tags = {
    "Name"               = "michelle.hernandez"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_iam_user_policy_attachment" "clouxter_michelle_hernandez_password" {
  user       = aws_iam_user.clouxter_michelle_hernandez.name
  policy_arn = "arn:aws:iam::aws:policy/IAMUserChangePassword"
}

resource "aws_iam_user_policy_attachment" "clouxter_michelle_hernandez_billing" {
  user       = aws_iam_user.clouxter_michelle_hernandez.name
  policy_arn = "arn:aws:iam::aws:policy/AWSBillingReadOnlyAccess"
}

resource "aws_iam_user_policy_attachment" "clouxter_michelle_hernandez_cloudtrail" {
  user       = aws_iam_user.clouxter_michelle_hernandez.name
  policy_arn = "arn:aws:iam::aws:policy/AWSCloudTrailReadOnlyAccess"
}

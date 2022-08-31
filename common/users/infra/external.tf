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

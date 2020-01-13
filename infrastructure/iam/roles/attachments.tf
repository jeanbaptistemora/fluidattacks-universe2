resource "aws_iam_policy_attachment" "SSO_Finance-attach2" {
  name       = "SSO_Finance-attachment2"
  roles     = ["${aws_iam_role.SSO_Finance.name}"]
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ReadOnlyAccess"
}

# SSO Attachments

resource "aws_iam_policy_attachment" "SSO-ec2full" {
  name       = "SSO-ec2full"
  roles     = ["${aws_iam_role.SSO.name}"]
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}
resource "aws_iam_policy_attachment" "SSO-codecommitfull" {
  name       = "SSO-codecommitfull"
  roles     = ["${aws_iam_role.SSO.name}"]
  policy_arn = "arn:aws:iam::aws:policy/AWSCodeCommitFullAccess"
}
resource "aws_iam_policy_attachment" "SSO-lambdafull" {
  name       = "SSO-lambdafull"
  roles     = ["${aws_iam_role.SSO.name}"]
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaFullAccess"
}
resource "aws_iam_policy_attachment" "SSO-iamfull" {
  name       = "SSO-iamfull"
  roles     = ["${aws_iam_role.SSO.name}"]
  policy_arn = "arn:aws:iam::aws:policy/IAMFullAccess"
}
resource "aws_iam_policy_attachment" "SSO-simworkfull" {
  name       = "SSO-simworkfull"
  roles     = ["${aws_iam_role.SSO.name}"]
  policy_arn = "arn:aws:iam::aws:policy/SimpleWorkflowFullAccess"
}
resource "aws_iam_policy_attachment" "SSO-s3full" {
  name       = "SSO-s3full"
  roles     = ["${aws_iam_role.SSO.name}"]
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}
resource "aws_iam_policy_attachment" "SSO-cloudtrailfull" {
  name       = "SSO-cloudtrailfull"
  roles     = ["${aws_iam_role.SSO.name}"]
  policy_arn = "arn:aws:iam::aws:policy/AWSCloudTrailFullAccess"
}
resource "aws_iam_policy_attachment" "SSO-admin" {
  name       = "SSO-admin"
  roles     = ["${aws_iam_role.SSO.name}"]
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}
resource "aws_iam_policy_attachment" "SSO-r53full" {
  name       = "SSO-r53full"
  roles     = ["${aws_iam_role.SSO.name}"]
  policy_arn = "arn:aws:iam::aws:policy/AmazonRoute53FullAccess"
}

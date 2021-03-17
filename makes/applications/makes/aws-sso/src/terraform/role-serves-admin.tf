resource "aws_iam_role" "serves-admin-role" {
  name                 = "serves-admin"
  assume_role_policy   = data.aws_iam_policy_document.okta-assume-role-policy-data.json
  max_session_duration = "32400"

  tags = {
    "Name"               = "serves-admin"
    "management:type"    = "production"
    "management:product" = "serves"
  }
}

resource "aws_iam_role_policy_attachment" "serves-admin-ec2" {
  role       = aws_iam_role.serves-admin-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2FullAccess"
}

resource "aws_iam_role_policy_attachment" "serves-admin-code-commit" {
  role       = aws_iam_role.serves-admin-role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSCodeCommitFullAccess"
}

resource "aws_iam_role_policy_attachment" "serves-admin-lambda" {
  role       = aws_iam_role.serves-admin-role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambdaFullAccess"
}

resource "aws_iam_role_policy_attachment" "serves-admin-iam" {
  role       = aws_iam_role.serves-admin-role.name
  policy_arn = "arn:aws:iam::aws:policy/IAMFullAccess"
}

resource "aws_iam_role_policy_attachment" "serves-admin-simple-worflow" {
  role       = aws_iam_role.serves-admin-role.name
  policy_arn = "arn:aws:iam::aws:policy/SimpleWorkflowFullAccess"
}

resource "aws_iam_role_policy_attachment" "serves-admin-s3" {
  role       = aws_iam_role.serves-admin-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

resource "aws_iam_role_policy_attachment" "serves-admin-sns" {
  role       = aws_iam_role.serves-admin-role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSCloudTrailFullAccess"
}

resource "aws_iam_role_policy_attachment" "serves-admin-admin" {
  role       = aws_iam_role.serves-admin-role.name
  policy_arn = "arn:aws:iam::aws:policy/AdministratorAccess"
}

resource "aws_iam_role_policy_attachment" "serves-admin-route-53" {
  role       = aws_iam_role.serves-admin-role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonRoute53FullAccess"
}

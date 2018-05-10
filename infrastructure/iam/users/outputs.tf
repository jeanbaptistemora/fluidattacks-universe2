output "fis3integration" {
  value = "${aws_iam_user.fis3integration.name}"
}
output "examss3" {
  value = "${aws_iam_user.examss3.name}"
}
output "fws3user" {
  value = "${aws_iam_user.fws3user.name}"
}


output "fis3integrationID" {
  value = "${aws_iam_access_key.fis3integration.id}"
}

output "cloudwatchID" {
  value = "${aws_iam_access_key.cloudwatch.id}"
}

output "fluidintegratesdynamoID" {
  value = "${aws_iam_access_key.fluidintegratesdynamo.id}"
}

output "fws3userID" {
  value = "${aws_iam_access_key.fws3user.id}"
}

#
output "fis3integrationSECRET" {
  value = "${aws_iam_access_key.fis3integration.secret}"
}

output "cloudwatchSECRET" {
  value = "${aws_iam_access_key.cloudwatch.secret}"
}

output "fluidintegratesdynamoSECRET" {
  value = "${aws_iam_access_key.fluidintegratesdynamo.secret}"
}

output "fws3userSECRET" {
  value = "${aws_iam_access_key.fws3user.secret}"
}

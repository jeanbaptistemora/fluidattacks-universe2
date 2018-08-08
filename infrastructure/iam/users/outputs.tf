output "fis3integration" {
  value = "${aws_iam_user.fis3integration.name}"
}

output "fiDynamo" {
  value  = "${aws_iam_user.fluidintegratesdynamo.name}"
}

output "fiS3Arn" {
  value = "${aws_iam_user.fis3integration.arn}"
}

output "examss3" {
  value = "${aws_iam_user.examss3.name}"
}

output "fws3user" {
  value = "${aws_iam_user.fws3user.name}"
}


output "fis3integrationID" {
  value = "${aws_iam_access_key.fis3integration2.id}"
}

output "cloudwatchID" {
  value = "${aws_iam_access_key.cloudwatch2.id}"
}

output "fluidintegratesdynamoID" {
  value = "${aws_iam_access_key.fluidintegratesdynamo2.id}"
}

output "fws3userID" {
  value = "${aws_iam_access_key.fws3user2.id}"
}

#
output "fis3integrationSECRET" {
  value = "${aws_iam_access_key.fis3integration2.secret}"
}

output "cloudwatchSECRET" {
  value = "${aws_iam_access_key.cloudwatch2.secret}"
}

output "fluidintegratesdynamoSECRET" {
  value = "${aws_iam_access_key.fluidintegratesdynamo2.secret}"
}

output "fws3userSECRET" {
  value = "${aws_iam_access_key.fws3user2.secret}"
}

resource "aws_iam_user" "fis3integration" {
  name = "FI_S3INTEGRATION"
  path = "/"
}

resource "aws_iam_access_key" "fis3integration" {
  user    = "${aws_iam_user.fis3integration.name}"
  provisioner "local-exec" {
   command = "echo ${aws_iam_access_key.fis3integration.id} >> ../../fis3integrationID.txt"
 }
 provisioner "local-exec" {
  command = "echo ${aws_iam_access_key.fis3integration.secret} >> ../../fis3integrationSECRET.txt"
}
}

resource "aws_iam_user" "cloudwatch" {
  name = "Cloudwatch"
  path = "/"
}

resource "aws_iam_access_key" "cloudwatch" {
  user    = "${aws_iam_user.cloudwatch.name}"
  provisioner "local-exec" {
   command = "echo ${aws_iam_access_key.cloudwatch.id} >> ../../cloudwatchID.txt"
 }
 provisioner "local-exec" {
  command = "echo ${aws_iam_access_key.cloudwatch.secret} >> ../../cloudwatchSECRET.txt"
}
}

resource "aws_iam_user" "fluidintegratesdynamo" {
  name = "FLUIDIntegratesDynamo"
  path = "/"
}

resource "aws_iam_access_key" "fluidintegratesdynamo" {
  user    = "${aws_iam_user.fluidintegratesdynamo.name}"
  provisioner "local-exec" {
   command = "echo ${aws_iam_access_key.fluidintegratesdynamo.id} >> ../../fluidintegratesdynamoID.txt"
 }
 provisioner "local-exec" {
  command = "echo ${aws_iam_access_key.fluidintegratesdynamo.secret} >> ../../fluidintegratesdynamoSECRET.txt"
}
}

resource "aws_iam_user" "fws3user" {
  name = "FW_S3_USER"
  path = "/"
}

resource "aws_iam_access_key" "fws3user" {
  user    = "${aws_iam_user.fws3user.name}"
  provisioner "local-exec" {
   command = "echo ${aws_iam_access_key.fws3user.id} >> ../../fws3userID.txt"
 }
 provisioner "local-exec" {
  command = "echo ${aws_iam_access_key.fws3user.secret} >> ../../fws3userSECRET.txt"
}
}

resource "aws_iam_user" "examss3" {
  name = "FS_EXAMS_S3"
  path = "/"
}

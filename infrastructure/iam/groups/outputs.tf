
output "fis3integration" {
  value = "${aws_iam_group.fis3integration.name}"
}

output "fluidserves" {
  value = "${aws_iam_group.fluidserves.name}"
}

output "web" {
  value = "${aws_iam_group.web.name}"
}

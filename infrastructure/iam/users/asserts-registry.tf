variable "asserts-clients" {
  type = "map"
}

resource "aws_iam_user" "asserts-clients" {
  count = "${length(var.asserts-clients)}"
  name = "asserts-${var.asserts-clients[count.index]}"
}

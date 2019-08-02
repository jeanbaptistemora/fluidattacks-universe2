variable "asserts-clients" {
  type = "map"
}

resource "aws_ecr_repository" "asserts-repos" {
  count = "${length(var.asserts-clients)}"
  name = "asserts-${var.asserts-clients[count.index]}"
}

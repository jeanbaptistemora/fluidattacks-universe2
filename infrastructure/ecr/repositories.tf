resource "aws_ecr_repository" "asserts-repos" {
  count = "${length(var.clients)}"
  name = "${var.clients[count.index]}"
}

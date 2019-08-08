variable "asserts_projects" {
  type = "map"
}

resource "aws_ecr_repository" "asserts-repos" {
  count = "${length(var.asserts_projects)}"
  name = "asserts-${var.asserts_projects[count.index]}"
}

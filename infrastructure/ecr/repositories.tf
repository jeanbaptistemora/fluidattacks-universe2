variable "asserts_projects" {
  type = list(string)
}

resource "aws_ecr_repository" "asserts-repos" {
  for_each = {for name in var.asserts_projects: name => name}
  name     = "asserts-${each.value}"
}

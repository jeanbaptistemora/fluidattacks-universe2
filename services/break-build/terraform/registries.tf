resource "aws_ecr_repository" "break-build-repos" {
  for_each = {for name in var.break_build_projects: name => name}
  name     = "break-build-${each.value}"
}

resource "aws_ecr_lifecycle_policy" "break-build-lifecicle-policies" {
  for_each   = {for name in var.break_build_projects: name => name}
  repository = aws_ecr_repository.break-build-repos[each.value].name

  policy = <<EOF
{
  "rules": [
    {
      "action": {
        "type": "expire"
      },
      "selection": {
        "countType": "imageCountMoreThan",
        "countNumber": 1,
        "tagStatus": "untagged"
      },
      "description": "Expire untagged images",
      "rulePriority": 1
    }
  ]
}
EOF
}

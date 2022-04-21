resource "aws_ecs_task_definition" "main" {
  family                   = "schedule"
  requires_compatibilities = ["EC2"]
  network_mode             = "host"
  task_role_arn            = data.aws_iam_role.prod_common.arn
  execution_role_arn       = data.aws_iam_role.prod_common.arn

  container_definitions = jsonencode(
    [
      {
        name   = "makes"
        image  = "ghcr.io/fluidattacks/makes:22.05"
        cpu    = 2048
        memory = 4096
      }
    ]
  )

  tags = {
    "Name"               = "schedule"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

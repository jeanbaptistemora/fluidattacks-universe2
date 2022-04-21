resource "aws_ecs_task_definition" "main" {
  family                   = "schedule"
  requires_compatibilities = ["EC2"]
  network_mode             = "host"

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

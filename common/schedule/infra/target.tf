
resource "aws_cloudwatch_event_target" "main" {
  for_each = local.schedules

  target_id = each.key
  rule      = aws_cloudwatch_event_rule.main[each.key].name
  arn       = aws_ecs_cluster.main.arn
  role_arn  = data.aws_iam_role.prod_common.arn

  input = jsonencode(
    {
      containerOverrides = [
        {
          name        = "makes"
          command     = each.value.command
          cpu         = each.value.cpu
          memory      = each.value.memory
          environment = each.value.environment
        }
      ]
    }
  )

  ecs_target {
    task_count          = 1
    task_definition_arn = aws_ecs_task_definition.main.arn
    launch_type         = "FARGATE"
    propagate_tags      = "TASK_DEFINITION"

    network_configuration {
      subnets          = [data.aws_subnet.common.id]
      security_groups  = [aws_security_group.main.id]
      assign_public_ip = true
    }

    tags = {
      "Name"               = each.key
      "management:area"    = "cost"
      "management:product" = "common"
      "management:type"    = "product"
    }
  }
}

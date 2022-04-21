resource "aws_cloudwatch_event_rule" "main" {
  for_each = local.schedules

  name                = each.key
  schedule_expression = each.value.schedule_expression

  tags = {
    "Name"               = each.key
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

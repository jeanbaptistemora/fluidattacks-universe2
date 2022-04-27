resource "aws_batch_job_queue" "default" {
  for_each = {
    for data in setproduct(
      local.compute_environment_names,
      local.queues,
    ) :

    "${data[0]}_${data[1].name}" => {
      compute_environment = data[0]
      priority            = data[1].priority
      tags                = local.compute_environments[data[0]].tags
    }
  }
  compute_environments = [
    aws_batch_compute_environment.default[each.value.compute_environment].arn
  ]
  name     = each.key
  priority = each.value.priority
  state    = "ENABLED"
  tags     = each.value.tags
}

resource "aws_batch_job_queue" "fargate" {
  for_each = local.environments.fargate

  name                 = "fargate_${each.key}"
  state                = "ENABLED"
  priority             = 1
  compute_environments = [aws_batch_compute_environment.fargate[each.key].arn]

  tags = {
    "Name"               = "fargate_${each.key}"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_batch_job_definition" "makes" {
  name = "makes"
  type = "container"
  container_properties = jsonencode(
    {
      image = "ghcr.io/fluidattacks/makes:22.05"

      # Will be overridden on job submission
      memory = 1800
      vcpus  = 1
  })

  tags = {
    "Name"               = "makes"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

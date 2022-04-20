resource "aws_batch_job_definition" "default" {
  name = "default"
  tags = {
    "Name"               = "default"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
  type = "container"

  # This can be overridden on a per-job basis so let's add default values
  container_properties = jsonencode({
    command = ["./build.sh", "--help"]
    image   = "registry.gitlab.com/fluidattacks/product/makes"
    memory  = 512
    vcpus   = 1
  })
}

resource "aws_batch_job_definition" "makes" {
  name = "makes"
  type = "container"
  container_properties = jsonencode({
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

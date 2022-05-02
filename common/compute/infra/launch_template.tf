resource "aws_launch_template" "batch_instance_regular" {
  block_device_mappings {
    device_name  = "/dev/xvdcz"
    virtual_name = "ephemeral0"
  }
  key_name = "gitlab"
  name     = "batch_instance_regular"

  tag_specifications {
    resource_type = "volume"

    tags = {
      "Name"               = "batch_instance_regular"
      "management:area"    = "cost"
      "management:product" = "common"
      "management:type"    = "product"
    }
  }

  tags = {
    "Name"               = "batch_instance_regular"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }

  user_data = filebase64("${path.module}/aws_batch_user_data")
}

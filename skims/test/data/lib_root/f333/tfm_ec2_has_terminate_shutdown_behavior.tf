resource "aws_launch_template" "foo" {

  name = "foo"

  block_device_mappings {
    device_name = "/dev/sda1"

    ebs {
      volume_size = 20
    }
  }

  iam_instance_profile {
    name = "test"
  }

  image_id                             = "ami-test"
  instance_initiated_shutdown_behavior = "stop"

}

resource "aws_launch_template" "foo" {

  name = "foo"

  block_device_mappings {
    device_name = "/dev/sda1"

    ebs {
      volume_size = 20
    }
  }

  iam_instance_profile {
    name = "test"
  }

  image_id                             = "ami-test"
  instance_initiated_shutdown_behavior = "terminate"

}

resource "aws_launch_template" "foo" {

  name = "foo"

  block_device_mappings {
    device_name = "/dev/sda1"

    ebs {
      volume_size = 20
    }
  }

  iam_instance_profile {
    name = "test"
  }

  image_id = "ami-test"

}

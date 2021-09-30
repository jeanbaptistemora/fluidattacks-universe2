variable "gitlabTokenFluidattacks" {}
variable "gitlabTokenAutonomicmind" {}
variable "gitlabTokenAutonomicjump" {}
variable "makesCiInit" {}

data "local_file" "init_runner" {
  filename = "${var.makesCiInit}/runner.sh"
}

data "local_file" "init_worker" {
  filename = "${var.makesCiInit}/worker.sh"
}

#
# Constants
#

variable "runner_ami" {
  type = map(list(string))
  default = {
    "name" = ["amzn2-ami-hvm-2.0.20210721.2-x86_64-ebs"]
  }
}

variable "worker_ami" {
  type = map(list(string))
  default = {
    "name"     = ["ubuntu/images/hvm-ssd/ubuntu-focal-20.04-amd64-server-20210907"],
    "image-id" = ["ami-03a80f322a6053f85"],
  }
}

variable "off_peak_periods" {
  type = list(object({
    periods    = list(string)
    idle_count = number
    idle_time  = number
    timezone   = string
  }))
  default = [
    {
      periods = [
        "* * 0-6,20-23 * * mon-fri *",
        "* * * * * sat,sun *",
      ]
      idle_count = 0
      idle_time  = 1800
      timezone   = "America/Bogota"
    }
  ]
}

variable "runner_block_device" {
  type = object({
    delete_on_termination = bool
    volume_type           = string
    volume_size           = number
    encrypted             = bool
    iops                  = number
  })
  default = {
    delete_on_termination = true
    volume_type           = "gp3"
    volume_size           = 15
    encrypted             = true
    iops                  = 3000
  }
}

variable "runner_timeout" {
  default = "86400"
}

#
# Reused infrastructure from other services
#

variable "autostaling_ci_vpc_id" {
  default = "vpc-0ea1c7bd6be683d2d"
}

variable "autoscaling_ci_subnet_id" {
  default = "subnet-0bceb7aa2c900324a"
}

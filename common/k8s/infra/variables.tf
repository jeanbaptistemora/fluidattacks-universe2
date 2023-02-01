locals {
  cluster_name = "common-k8s"
}

data "aws_caller_identity" "main" {}
data "aws_security_group" "cloudflare" {
  name = "CloudFlare"
}
data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["fluid-vpc"]
  }
}
data "aws_subnet" "main" {
  for_each = toset([
    "k8s_1",
    "k8s_2",
    "k8s_3",
    "k8s_4",
    "k8s_5",
    "k8s_6",
    "k8s_7",
    "k8s_8",
    "k8s_9",
    "k8s_10",
  ])

  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = [each.key]
  }
}

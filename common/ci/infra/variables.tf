variable "gitlabRunnerToken" {}

# Reused infrastructure from other services

data "aws_caller_identity" "main" {}
data "aws_vpc" "main" {
  filter {
    name   = "tag:Name"
    values = ["fluid-vpc"]
  }
}
data "aws_subnet" "main" {
  vpc_id = data.aws_vpc.main.id
  filter {
    name   = "tag:Name"
    values = ["ci"]
  }
}

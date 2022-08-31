resource "aws_cloudwatch_log_group" "job" {
  name = "/aws/batch/job"

  tags = {
    "Name"               = "job"
    "Management:Area"    = "cost"
    "Management:Product" = "common"
    "Management:Type"    = "product"
  }
}

resource "aws_cloudwatch_log_group" "skims" {
  name = "skims"

  tags = {
    "Name"               = "skims"
    "Management:Area"    = "cost"
    "Management:Product" = "skims"
    "Management:Type"    = "product"
  }
}

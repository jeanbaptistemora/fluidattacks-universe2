resource "aws_cloudwatch_log_group" "fluid" {
  name = "FLUID"

  tags = {
    "Name"               = "FLUID"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

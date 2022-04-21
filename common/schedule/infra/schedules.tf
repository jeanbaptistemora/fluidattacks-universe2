# Schedule expressions:
# https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html

locals {
  schedules = {
    common_criteria_test_base = {
      cpu     = 1024
      memory  = 2048
      command = ["m", "f", "/common/criteria/test/base"]

      schedule_expression = "cron(0/5 * * * ? *)"

      environment = {
        "PRODUCT_API_TOKEN" = var.productApiToken
      }
    }
  }
}

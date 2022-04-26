# Schedule expressions:
# https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html

locals {
  schedules = {
    common_criteria_test_base = {
      enabled = true
      command = ["m", "f", "/common/criteria/test/base"]

      schedule_expression = "cron(0/5 * * * ? *)"
      cpu                 = 1024
      memory              = 2048
      storage             = 25

      environment = {
        PRODUCT_API_TOKEN = var.productApiToken
      }
    }
  }
}

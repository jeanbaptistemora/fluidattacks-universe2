resource "checkly_check" "integrates_web" {
  name                      = "ASM"
  type                      = "BROWSER"
  activated                 = true
  frequency                 = 10
  double_check              = true
  ssl_check                 = true
  use_global_alert_settings = false
  runtime_id                = "2021.06"
  group_id                  = checkly_check_group.fluidattacks.id
  group_order               = 3

  locations = ["us-east-1"]

  script = <<-EOF
    const assert = require("chai").assert;
    const playwright = require("playwright");

    const browser = await playwright.chromium.launch();
    const page = await browser.newPage();
    await page.goto("https://app.fluidattacks.com");
    const title = await page.title();

    assert.equal(title, "Fluid Attacks");
    await browser.close();
  EOF
}

resource "checkly_check" "integrates_api" {
  name                      = "API"
  type                      = "API"
  activated                 = true
  frequency                 = 10
  double_check              = true
  ssl_check                 = true
  use_global_alert_settings = false
  runtime_id                = "2021.10"
  group_id                  = checkly_check_group.fluidattacks.id
  group_order               = 4

  locations = ["us-east-1"]

  request {
    url              = "https://app.fluidattacks.com/api"
    follow_redirects = true
    body_type        = "GRAPHQL"
    method           = "POST"

    headers = {
      authorization = "Bearer {{INTEGRATES_API_TOKEN}}"
    }

    assertion {
      source     = "TEXT_BODY"
      property   = "(.*)"
      comparison = "CONTAINS"
      target     = "abuja"
    }
    assertion {
      source     = "TEXT_BODY"
      property   = "(.*)"
      comparison = "CONTAINS"
      target     = "imamura"
    }

    body = <<-EOF
      query ChecklyApiCheck {
        me {
          organizations {
            name
          groups {
            name
          }
        }
          remember
        }
        organization(organizationId: "ORG#0d6d8f9d-3814-48f8-ba2c-f4fb9f8d4ffa") {
          userRole
          groups {
            name
          }
        }
        group(groupName: "abuja") {
          permissions
          findings {
            vulnerabilities(state: "open") {
              id
          where
            }
          }
        }
      }
    EOF
  }
}

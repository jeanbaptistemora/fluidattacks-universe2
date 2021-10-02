resource "checkly_check" "docs" {
  name                      = "Docs"
  type                      = "BROWSER"
  activated                 = true
  frequency                 = 10
  double_check              = true
  ssl_check                 = true
  use_global_alert_settings = false
  runtime_id                = "2021.06"
  group_id                  = checkly_check_group.fluidattacks.id

  locations = ["us-east-1"]

  script = <<-EOF
    const assert = require("chai").assert;
    const puppeteer = require("puppeteer");

    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto("https://docs.fluidattacks.com/");
    const title = await page.title();

    assert.equal(title, "Fluid Attacks Documentation | Fluid Attacks Documentation");
    await browser.close();
  EOF
}

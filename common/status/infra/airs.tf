resource "checkly_check" "airs" {
  name                      = "WEB"
  type                      = "BROWSER"
  activated                 = true
  frequency                 = 10
  double_check              = true
  ssl_check                 = true
  use_global_alert_settings = false
  runtime_id                = "2021.10"
  group_id                  = checkly_check_group.fluidattacks.id
  group_order               = 1

  locations = ["us-east-1"]

  script = <<-EOF
    const assert = require("chai").assert;
    const playwright = require("playwright");

    const browser = await playwright.chromium.launch();
    const page = await browser.newPage();
    await page.goto("https://fluidattacks.com/", {
      waitUntil: "domcontentloaded"
    });
    const title = await page.title();

    assert.equal(title, "Application security testing solutions | Fluid Attacks");
    await browser.close();
  EOF
}

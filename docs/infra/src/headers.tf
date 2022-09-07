# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "cloudflare_worker_script" "headers" {
  name    = "docs_headers"
  content = file("js/headers.js")
}


# Production

resource "cloudflare_worker_route" "headers_prod" {
  zone_id     = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  pattern     = "docs.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}/*"
  script_name = cloudflare_worker_script.headers.name
}


# Development

resource "cloudflare_worker_route" "headers_dev" {
  zone_id     = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  pattern     = "docs-dev.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}/*"
  script_name = cloudflare_worker_script.headers.name
}

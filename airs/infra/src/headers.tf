# Common

resource "cloudflare_worker_script" "main" {
  name    = "airs_headers"
  content = file("js/headers.js")
}

# Production

resource "cloudflare_worker_route" "prod" {
  zone_id     = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  pattern     = "${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}/*"
  script_name = cloudflare_worker_script.main.name
}


# Development

resource "cloudflare_worker_route" "dev" {
  zone_id     = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  pattern     = "web.eph.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}/*"
  script_name = cloudflare_worker_script.main.name
}

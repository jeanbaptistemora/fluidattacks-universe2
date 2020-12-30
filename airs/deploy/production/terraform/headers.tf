resource "cloudflare_worker_script" "headers" {
  name    = "airs_production_headers"
  content = file("js/headers.js")
}

resource "cloudflare_worker_route" "headers" {
  zone_id     = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  pattern     = "${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}/*"
  script_name = cloudflare_worker_script.headers.name
}

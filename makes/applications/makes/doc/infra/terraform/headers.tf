resource "cloudflare_worker_script" "headers" {
  name    = "doc_headers"
  content = file("js/headers.js")
}


# Production


resource "cloudflare_worker_route" "headers_prod" {
  zone_id     = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  pattern     = "doc.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}/*"
  script_name = cloudflare_worker_script.headers.name
}


# Development

resource "cloudflare_worker_route" "headers_dev" {
  zone_id     = lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "id")
  pattern     = "doc.dev.${lookup(data.cloudflare_zones.fluidattacks_com.zones[0], "name")}/*"
  script_name = cloudflare_worker_script.headers.name
}

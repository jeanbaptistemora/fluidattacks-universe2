resource "cloudflare_certificate_pack" "main" {
  zone_id               = cloudflare_zone.fluidattacks_com.id
  type                  = "advanced"
  validation_method     = "txt"
  validity_days         = 30
  certificate_authority = "digicert"
  cloudflare_branding   = false

  hosts = [
    cloudflare_zone.fluidattacks_com.zone,
    "*.${cloudflare_zone.fluidattacks_com.zone}",
    "*.app.${cloudflare_zone.fluidattacks_com.zone}",
    "*.integrates.${cloudflare_zone.fluidattacks_com.zone}",
    "*.front.production.${cloudflare_zone.fluidattacks_com.zone}",
    "*.front.development.${cloudflare_zone.fluidattacks_com.zone}",
    "*.eph.${cloudflare_zone.fluidattacks_com.zone}",
  ]

  lifecycle {
    create_before_destroy = true
  }
}

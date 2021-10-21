# CloudFlare

output "api_token_airs_production" {
  sensitive = true
  value     = cloudflare_api_token.airs_production.value
}

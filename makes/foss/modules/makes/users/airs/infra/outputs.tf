# CloudFlare

output "api_token_airs_development" {
  sensitive = true
  value     = cloudflare_api_token.airs_development.value
}

output "api_token_airs_production" {
  sensitive = true
  value     = cloudflare_api_token.airs_production.value
}

# CloudFlare

output "api_token_integrates_development" {
  sensitive = true
  value     = cloudflare_api_token.integrates_development.value
}

output "api_token_integrates_production" {
  sensitive = true
  value     = cloudflare_api_token.integrates_production.value
}

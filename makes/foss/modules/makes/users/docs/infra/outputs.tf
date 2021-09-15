# CloudFlare

output "dev_api_token" {
  sensitive = true
  value     = cloudflare_api_token.dev.value
}

output "prod_api_token" {
  sensitive = true
  value     = cloudflare_api_token.prod.value
}

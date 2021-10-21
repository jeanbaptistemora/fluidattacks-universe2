# CloudFlare

output "prod_api_token" {
  sensitive = true
  value     = cloudflare_api_token.prod.value
}

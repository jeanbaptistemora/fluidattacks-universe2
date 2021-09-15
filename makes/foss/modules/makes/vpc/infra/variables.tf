variable "cloudflare_email" {}
variable "cloudflare_api_key" {}

data "aws_caller_identity" "current" {}
data "cloudflare_ip_ranges" "cloudflare" {}

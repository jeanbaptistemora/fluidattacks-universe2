resource "aws_security_group" "cloudflare" {
  name        = "CloudFlare"
  description = "Access to CloudFlare IP Ranges"
  vpc_id      = aws_vpc.fluid-vpc.id

  ingress {
    description = "cloudflare-access"
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = data.cloudflare_ip_ranges.cloudflare.ipv4_cidr_blocks
  }

  tags = {
    "Name"               = "CloudFlare"
    "management:area"    = "cost"
    "management:product" = "common"
    "management:type"    = "product"
  }
}

resource "aws_security_group" "cloudflare" {
  name        = "CloudFlare"
  description = "Access to CloudFlare IP Ranges"
  vpc_id      = aws_vpc.fluid-vpc.id

  ingress {
    description = "cloudflare-access"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = data.cloudflare_ip_ranges.cloudflare.ipv4_cidr_blocks
    self        = true
  }

  egress {
    description = "default-aws-egress-rule"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    "Name"               = "CloudFlare"
    "management:area"    = "cost"
    "management:product" = "makes"
    "management:type"    = "product"
  }
}

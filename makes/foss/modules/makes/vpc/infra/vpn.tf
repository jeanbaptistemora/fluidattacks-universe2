resource "aws_vpn_gateway" "medellin" {
  vpc_id = aws_vpc.fluid-vpc.id

  tags = {
    "Name"               = "medellin-vpn-gateway"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_customer_gateway" "medellin" {
  bgp_asn     = 65000
  ip_address  = "190.217.110.94"
  type        = "ipsec.1"
  device_name = "Router medellin"

  tags = {
    "Name"               = "medellin-customer-gateway"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

resource "aws_vpn_connection" "medellin" {
  vpn_gateway_id      = aws_vpn_gateway.medellin.id
  customer_gateway_id = aws_customer_gateway.medellin.id
  type                = "ipsec.1"

  static_routes_only       = true
  local_ipv4_network_cidr  = "172.30.56.0/24"
  remote_ipv4_network_cidr = "192.168.8.0/23"

  tags = {
    "Name"               = "medellin-vpn-connection"
    "management:type"    = "production"
    "management:product" = "makes"
  }
}

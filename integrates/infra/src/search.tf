resource "aws_opensearch_domain" "integrates" {
  domain_name    = "integrates"
  engine_version = "OpenSearch_1.2"

  cluster_config {
    instance_type = "t3.small.search"
  }

  encrypt_at_rest {
    enabled = true
  }

  tags = {
    "Name"               = "integrates-opensearch"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

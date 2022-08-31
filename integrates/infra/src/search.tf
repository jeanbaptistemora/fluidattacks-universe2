resource "aws_security_group" "integrates-opensearch" {
  name   = "integrates-opensearch"
  vpc_id = data.aws_vpc.main.id

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.main.cidr_block]
  }

  egress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.main.cidr_block]
  }

  tags = {
    "Name"               = "integrates-opensearch"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
  }
}

resource "aws_iam_service_linked_role" "integrates-opensearch" {
  aws_service_name = "opensearchservice.amazonaws.com"
}

resource "aws_opensearch_domain" "integrates" {
  depends_on     = [aws_iam_service_linked_role.integrates-opensearch]
  domain_name    = "integrates"
  engine_version = "OpenSearch_1.3"

  cluster_config {
    instance_count         = 3
    instance_type          = "t3.small.search"
    zone_awareness_enabled = true
    zone_awareness_config {
      availability_zone_count = 3
    }
  }

  ebs_options {
    ebs_enabled = true
    volume_size = 10
  }

  encrypt_at_rest {
    enabled = true
  }

  log_publishing_options {
    cloudwatch_log_group_arn = aws_cloudwatch_log_group.fluid.arn
    log_type                 = "INDEX_SLOW_LOGS"
  }

  vpc_options {
    security_group_ids = [
      aws_security_group.integrates-opensearch.id,
    ]

    subnet_ids = [
      for subnet in data.aws_subnet.main : subnet.id
    ]
  }

  tags = {
    "Name"               = "integrates-opensearch"
    "Management:Area"    = "cost"
    "Management:Product" = "integrates"
    "Management:Type"    = "product"
  }
}

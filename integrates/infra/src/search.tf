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

resource "aws_iam_role" "opensearch_dynamodb_lambda_role" {
  name = "opensearch_dynamodb_lambda_role"

  assume_role_policy = <<-EOF
    {
      "Version": "2012-10-17",
      "Statement": [
        {
          "Action": "sts:AssumeRole",
          "Effect": "Allow",
          "Principal": {
            "Service": "lambda.amazonaws.com"
          },
          "Sid": ""
        }
      ]
    }
  EOF

  tags = {
    "Name"               = "integrates-opensearch"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

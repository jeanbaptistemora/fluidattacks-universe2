# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "aws_elasticache_subnet_group" "cache_db" {
  name = "integrates-cache"
  subnet_ids = [
    for subnet in data.aws_subnet.main : subnet.id
  ]
}

resource "aws_security_group" "cache_db" {
  name   = "integrates_cache"
  vpc_id = data.aws_vpc.main.id

  ingress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.main.cidr_block]
  }

  egress {
    from_port   = 6379
    to_port     = 6379
    protocol    = "tcp"
    cidr_blocks = [data.aws_vpc.main.cidr_block]
  }

  tags = {
    "Name"               = "integrates_cache"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

resource "aws_elasticache_replication_group" "cache_db" {
  # tflint-ignore: aws_elasticache_replication_group_default_parameter_group
  parameter_group_name          = "default.redis6.x.cluster.on"
  replication_group_id          = "integrates-cache"
  replication_group_description = "Integrates Redis cache"
  node_type                     = "cache.t3.micro"
  subnet_group_name             = aws_elasticache_subnet_group.cache_db.name
  automatic_failover_enabled    = true
  at_rest_encryption_enabled    = true
  transit_encryption_enabled    = false
  port                          = 6379

  security_group_ids = [
    aws_security_group.cache_db.id,
  ]

  cluster_mode {
    num_node_groups         = 6
    replicas_per_node_group = 1
  }

  tags = {
    "Name"               = "integrates-cache"
    "management:area"    = "cost"
    "management:product" = "integrates"
    "management:type"    = "product"
  }
}

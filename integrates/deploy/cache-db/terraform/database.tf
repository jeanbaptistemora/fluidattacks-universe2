resource "aws_elasticache_subnet_group" "cache_db" {
  name       = "integrates-cache"
  subnet_ids = var.subnets
}

resource "aws_elasticache_replication_group" "cache_db" {
  replication_group_id          = "integrates-cache"
  replication_group_description = "Integrates Redis cache"
  node_type                     = "cache.t3.micro"
  parameter_group_name          = "default.redis6.x.cluster.on"
  subnet_group_name             = aws_elasticache_subnet_group.cache_db.name
  automatic_failover_enabled    = true
  at_rest_encryption_enabled    = true
  transit_encryption_enabled    = false
  port                          = 6379
  security_group_ids = var.security_groups

  cluster_mode {
    num_node_groups         = 2
    replicas_per_node_group = 5
  }

  tags = {
    "Name"               = "integrates-cache"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_dax_subnet_group" "main" {
  name       = "integrates-cache"
  subnet_ids = var.subnets
}

resource "aws_dax_parameter_group" "main" {
  name = "integrates-cache"

  parameters {
    name  = "query-ttl-millis"
    value = "300000"
  }

  parameters {
    name  = "record-ttl-millis"
    value = "1800000"
  }
}

resource "aws_dax_cluster" "main" {
  cluster_name           = "integrates-cache"
  description            = "Integrates DAX Cluster"
  iam_role_arn           = data.aws_iam_role.dax_role.arn
  security_group_ids     = var.security_groups
  subnet_group_name      = aws_dax_subnet_group.main.name
  parameter_group_name   = aws_dax_parameter_group.main.name
  node_type              = "dax.r5.large"
  replication_factor     = 1
  maintenance_window     = "sun:10:00-sun:11:00"

  server_side_encryption {
    enabled = true
  }

  tags = {
    "Name"               = "integrates-cache"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

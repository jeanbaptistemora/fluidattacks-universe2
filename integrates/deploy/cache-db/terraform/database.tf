resource "aws_elasticache_subnet_group" "cache-db" {
  name       = "integrates-cache-db-subnet-group"
  subnet_ids = var.eks-subnets
}

resource "aws_elasticache_replication_group" "cache-db" {
  replication_group_id          = "integrates-cache-db"
  replication_group_description = "Integrates Redis cache-db"
  node_type                     = "cache.t2.medium"
  parameter_group_name          = "default.redis5.0.cluster.on"
  subnet_group_name             = aws_elasticache_subnet_group.cache-db.name
  automatic_failover_enabled    = true
  at_rest_encryption_enabled    = true
  transit_encryption_enabled    = false
  port                          = 6379

  cluster_mode {
    replicas_per_node_group = 1
    num_node_groups         = 1
  }

  tags = {
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

resource "aws_elasticache_subnet_group" "cache_db" {
  name       = "integrates-cache"
  subnet_ids = var.subnets
}

resource "aws_elasticache_replication_group" "cache_db" {
  replication_group_id          = "integrates-cache"
  replication_group_description = "Integrates Redis cache"
  node_type                     = "cache.t2.medium"
  parameter_group_name          = "default.redis5.0.cluster.on"
  subnet_group_name             = aws_elasticache_subnet_group.cache_db.name
  automatic_failover_enabled    = true
  at_rest_encryption_enabled    = true
  transit_encryption_enabled    = false
  port                          = 6379
  security_group_ids = var.security_groups

  cluster_mode {
    replicas_per_node_group = 1
    num_node_groups         = 1
  }

  tags = {
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

variable "cacheGroupId" {}
variable "cacheGroupDescription" {}
variable "cacheNodeType" {}
variable "cacheParamGroupName" {}
variable "k8sSubnet" {
  type = list(string)
}


resource "aws_elasticache_subnet_group" "redis-subnet-group" {
  name       = "redis-subnet-group"
  subnet_ids = var.k8sSubnet
}

resource "aws_elasticache_replication_group" "rediscache" {
  replication_group_id          = var.cacheGroupId
  replication_group_description = var.cacheGroupDescription
  node_type                     = var.cacheNodeType
  port                          = 6379
  parameter_group_name          = var.cacheParamGroupName
  automatic_failover_enabled    = true
  at_rest_encryption_enabled    = true
  transit_encryption_enabled	  = false
  subnet_group_name		          = "redis-subnet-group"

  cluster_mode {
    replicas_per_node_group = 1
    num_node_groups         = 1
  }
}

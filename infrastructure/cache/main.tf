variable "cacheGroupId" {}
variable "cacheGroupDescription" {}
variable "cacheNodeType" {}
variable "cacheParamGroupName" {}

resource "aws_elasticache_replication_group" "rediscache" {
  replication_group_id          = "${var.cacheGroupId}"
  replication_group_description = "${var.cacheGroupDescription}"
  node_type                     = "${var.cacheNodeType}"
  port                          = 6379
  parameter_group_name          = "${var.cacheParamGroupName}"
  automatic_failover_enabled    = true

  cluster_mode {
    replicas_per_node_group = 1
    num_node_groups         = 2
  }
}

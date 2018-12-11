variable "cacheGroupId" {}
variable "cacheGroupDescription" {}
variable "cacheNodeType" {}
variable "cacheParamGroupName" {}
variable "eksSnetReg" {
  type = "list"
}
variable "cacheCidr" {}
variable "vpcId" {}

resource "aws_subnet" "redis_subnet" {
  count = 2
  availability_zone = "${var.eksSnetReg[count.index]}"
  cidr_block        = "${cidrsubnet(var.cacheCidr, 2, count.index + 2)}"
  vpc_id            = "${var.vpcId}"

  tags = "${
    map(
     "Name", "redis_subnet",
    )
  }"
}

resource "aws_elasticache_subnet_group" "redis-subnet-group" {
  name       = "redis-subnet-group"
  subnet_ids = ["${aws_subnet.redis_subnet.*.id}"]
}

resource "aws_elasticache_replication_group" "rediscache" {
  replication_group_id          = "${var.cacheGroupId}"
  replication_group_description = "${var.cacheGroupDescription}"
  node_type                     = "${var.cacheNodeType}"
  port                          = 6379
  parameter_group_name          = "${var.cacheParamGroupName}"
  automatic_failover_enabled    = true
  at_rest_encryption_enabled    = true
  transit_encryption_enabled	= true
  subnet_group_name		= "redis-subnet-group"

  cluster_mode {
    replicas_per_node_group = 2
    num_node_groups         = 3
  }
}

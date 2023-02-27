variable "clusterUser" {
  default = "fakeUser"
}
variable "clusterPass" {
  default = "fakePassword1234"
}
# Network
resource "aws_security_group" "expose-redshift" {
  name        = "expose-redshift"
  description = "Expose redshift endpoint"
  vpc_id      = data.aws_vpc.main.id
  ingress {
    description      = "External access"
    from_port        = 5439
    to_port          = 5439
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  egress {
    description      = "VPC access"
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }
  tags = {
    "Name"               = "observes"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}
resource "aws_redshift_subnet_group" "main" {
  name = "observes"
  subnet_ids = [
    for subnet in data.aws_subnet.main : subnet.id
  ]

  tags = {
    "Name"               = "observes"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}
# Cluster
resource "aws_redshift_cluster" "main" {
  cluster_identifier = "observes"
  database_name      = "observes"
  master_username    = var.clusterUser
  master_password    = var.clusterPass

  cluster_type    = "multi-node"
  node_type       = "dc2.large"
  number_of_nodes = 2

  publicly_accessible  = true
  encrypted            = true
  enhanced_vpc_routing = true

  cluster_subnet_group_name = aws_redshift_subnet_group.main.name
  vpc_security_group_ids    = [aws_security_group.expose-redshift.id]

  preferred_maintenance_window        = "sun:04:00-sun:05:00"
  automated_snapshot_retention_period = 7
  iam_roles                           = [data.aws_iam_role.observes_redshift_cluster.arn]

  tags = {
    "Name"               = "observes"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}

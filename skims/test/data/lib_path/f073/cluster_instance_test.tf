resource "aws_db_instance" "default" {
  publicly_accessible  = true
  allocated_storage    = 10
  engine               = "mysql"
  engine_version       = "5.7"
  deletion_protection  = true
  instance_class       = "db.t3.micro"
  name                 = "mydb"
  username             = "foo"
  password             = "foobarbaz"
  parameter_group_name = "default.mysql5.7"
  skip_final_snapshot  = true
}

resource "aws_rds_cluster_instance" "cluster_instances" {
  count               = 2
  publicly_accessible = true
  identifier          = "aurora-cluster-demo-${count.index}"
  cluster_identifier  = aws_rds_cluster.default.id
  instance_class      = "db.r4.large"
  engine              = aws_rds_cluster.default.engine
  engine_version      = aws_rds_cluster.default.engine_version
}

resource "aws_rds_cluster" "default" {
  cluster_identifier  = "aurora-cluster-demo"
  availability_zones  = ["us-west-2a", "us-west-2b", "us-west-2c"]
  deletion_protection = true
  database_name       = "mydb"
  master_username     = "foo"
  master_password     = "barbut8chars"
}

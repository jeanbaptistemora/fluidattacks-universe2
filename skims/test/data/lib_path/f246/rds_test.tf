resource "aws_db_instance" "default" {
  allocated_storage       = 10
  storage_encrypted       = false
  engine                  = "mysql"
  engine_version          = "5.7"
  instance_class          = "db.t3.micro"
  name                    = "mydb"
  username                = "foo"
  deletion_protection     = true
  password                = "foobarbaz"
  backup_retention_period = 2
  parameter_group_name    = "default.mysql5.7"
  skip_final_snapshot     = true
}


resource "aws_rds_cluster" "postgresql" {
  cluster_identifier      = "aurora-cluster-demo"
  engine                  = "aurora-postgresql"
  availability_zones      = ["us-west-2a", "us-west-2b", "us-west-2c"]
  database_name           = "mydb"
  master_username         = "foo"
  master_password         = "bar"
  deletion_protection     = true
  backup_retention_period = 5
  preferred_backup_window = "07:00-09:00"
}

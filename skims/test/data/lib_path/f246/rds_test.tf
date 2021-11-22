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

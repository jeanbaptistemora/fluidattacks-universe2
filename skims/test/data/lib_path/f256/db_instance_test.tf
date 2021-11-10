resource "aws_db_instance" "default" {
  allocated_storage    = 10
  deletion_protection  = false
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t3.micro"
  name                 = "mydb"
  username             = "foo"
  password             = "foobarbaz"
  parameter_group_name = "default.mysql5.7"
  skip_final_snapshot  = true
}

resource "aws_db_instance" "test" {
  allocated_storage    = 10
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t3.micro"
  name                 = "mydb"
  username             = "user"
  password             = "useradmin"
  parameter_group_name = "default.mysql5.7"
  skip_final_snapshot  = true
}

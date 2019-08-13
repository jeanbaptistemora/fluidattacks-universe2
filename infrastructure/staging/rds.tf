resource "aws_db_subnet_group" "default" {
  name       = "main_dev"
  subnet_ids = aws_subnet.dev_subnet.*.id
}

resource "aws_db_parameter_group" "dev-parameter-group" {
  name   = "dev-parameter-group"
  family = "mysql5.6"

  parameter {
    name  = "character_set_server"
    value = "utf8"
  }
}

resource "aws_db_instance" "fluiddb_dev" {
  apply_immediately       = true
  allocated_storage       = 10
  storage_type            = var.storageType
  engine                  = var.engine
  engine_version          = var.engineVersion
  instance_class          = var.instanceClass
  name                    = var.dbDevName
  username                = var.dbDevUser
  password                = var.dbDevPass
  db_subnet_group_name    = aws_db_subnet_group.default.id
  parameter_group_name    = aws_db_parameter_group.dev-parameter-group.id
  skip_final_snapshot     = true
  publicly_accessible     = true
  maintenance_window      = "sun:05:00-sun:05:30"
  backup_retention_period = 7
  backup_window           = "06:00-06:30"
  lifecycle {
    ignore_changes = [snapshot_identifier]
  }
}

output "dbDevEndpoint" {
  value = "dbDevInstance=\"${aws_db_instance.fluiddb_dev.address}\""
}


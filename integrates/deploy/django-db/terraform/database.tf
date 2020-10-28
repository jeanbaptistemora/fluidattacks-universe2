resource "aws_db_instance" "django-db" {
  allocated_storage         = 10
  backup_retention_period   = 7
  backup_window             = "06:00-06:30"
  maintenance_window        = "sun:05:00-sun:05:30"
  engine                    = "mysql"
  engine_version            = "8.0.16"
  final_snapshot_identifier = "django-db-last-snapshot"
  identifier                = "django-db"
  instance_class            = "db.t3.small"
  ca_cert_identifier        = "rds-ca-2019"
  db_subnet_group_name      = aws_db_subnet_group.django-db.id
  name                      = "django"
  username                  = var.db_user
  password                  = var.db_password
  vpc_security_group_ids    = [aws_security_group.django-db.id]
  apply_immediately         = true
  skip_final_snapshot       = false
  publicly_accessible       = true

  tags = {
    "Name"               = "django"
    "management:type"    = "production"
    "management:product" = "integrates"
  }
}

output "endpoint" {
  value = aws_db_instance.django-db.address
}

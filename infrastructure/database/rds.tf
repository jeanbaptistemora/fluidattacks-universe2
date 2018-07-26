variable "storageType" {}
variable "engine" {}
variable "engineVersion" {}
variable "instanceClass" {}
variable "dbName" {}
variable "dbUser" {}
variable "dbPass" {}
variable "dbSnapId" {}

resource "aws_db_subnet_group" "default" {
  name       = "main"
  subnet_ids = ["${aws_subnet.rds_snet1.id}", "${aws_subnet.rds_snet2.id}",
                "${aws_subnet.rds_snet3.id}", "${aws_subnet.rds_snet4.id}",
                "${aws_subnet.rds_snet5.id}"]
}

resource "aws_db_parameter_group" "default" {
  name   = "default"
  family = "mysql5.6"

  parameter {
    name  = "character_set_server"
    value = "utf8"
  }
}

resource "aws_db_instance" "fluiddb" {
  apply_immediately = true
  allocated_storage    = 10
  storage_type         = "${var.storageType}"
  engine               = "${var.engine}"
  engine_version       = "${var.engineVersion}"
  instance_class       = "${var.instanceClass}"
  name                 = "${var.dbName}"
  username             = "${var.dbUser}"
  password             = "${var.dbPass}"
  db_subnet_group_name = "${aws_db_subnet_group.default.id}"
  parameter_group_name = "${aws_db_parameter_group.default.id}"
  snapshot_identifier = "${var.dbSnapId}"
  skip_final_snapshot  = true
  publicly_accessible = true
  maintenance_window = "sun:05:00-sun:05:30"
  backup_retention_period = 7
  backup_window = "06:00-06:30"
  lifecycle {
    ignore_changes = ["snapshot_identifier"]
  }
}

output "endpoint" {
  value = "${aws_db_instance.fluiddb.address}"

}

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

resource "aws_db_parameter_group" "fluid-database" {
  name   = "fluid-database"
  family = "mysql5.6"
  description = "Parameter Group for fluid-database"

  parameter{
    name = "wait_timeout"
    value = 900
  }
}

resource "aws_db_instance" "fluid-database" {
  allocated_storage         = 10
  apply_immediately         = true
  backup_retention_period   = 7
  backup_window             = "06:00-06:30"
  db_subnet_group_name      = "${aws_db_subnet_group.default.id}"
  engine                    = "${var.engine}"
  engine_version            = "${var.engineVersion}"
  final_snapshot_identifier = "fluid-database-last-snapshot"
  identifier                = "fluid-database"
  instance_class            = "${var.instanceClass}"
  maintenance_window        = "sun:05:00-sun:05:30"
  name                      = "${var.dbName}"
  parameter_group_name      = "${aws_db_parameter_group.fluid-database.id}"
  password                  = "${var.dbPass}"
  publicly_accessible       = true
  skip_final_snapshot       = false
  username                  = "${var.dbUser}"
  ca_cert_identifier        = "rds-ca-2019"
}

output "endpoint" {
  value = "${aws_db_instance.fluid-database.address}"

}

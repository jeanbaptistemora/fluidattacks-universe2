resource "aws_rds_cluster" "example" {
  cluster_identifier   = "example"
  deletion_protection  = false
  db_subnet_group_name = aws_db_subnet_group.example.name
  engine_mode          = "multimaster"
  master_password      = "barbarbarbar"
  master_username      = "foo"
  skip_final_snapshot  = true
}

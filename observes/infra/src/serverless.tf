resource "aws_redshiftserverless_namespace" "main" {
  namespace_name = "prod"
  iam_roles      = [data.aws_iam_role.observes_redshift_cluster.arn]
  tags = {
    "Name"               = "redshift_serverless_prod_namespace"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}

resource "aws_redshiftserverless_workgroup" "main" {
  namespace_name      = aws_redshiftserverless_namespace.main.id
  workgroup_name      = "observes"
  publicly_accessible = false
  subnet_ids = [
    for subnet in data.aws_subnet.main : subnet.id
  ]
  security_group_ids = [aws_security_group.expose-redshift.id]
  tags = {
    "Name"               = "redshift_serverless_observes_workgroup"
    "management:area"    = "cost"
    "management:product" = "observes"
    "management:type"    = "product"
  }
}

resource "aws_redshiftserverless_usage_limit" "main" {
  resource_arn  = aws_redshiftserverless_workgroup.main.arn
  usage_type    = "serverless-compute"
  amount        = 800
  period        = "daily"
  breach_action = "deactivate"
}

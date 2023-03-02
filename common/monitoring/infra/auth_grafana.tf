data "aws_iam_policy_document" "grafana_sts" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"

    principals {
      identifiers = ["grafana.amazonaws.com"]
      type        = "Service"
    }
  }
}

data "aws_iam_policy_document" "grafana_athena_access" {
  statement {
    actions   = ["athena:ListDataCatalogs"]
    effect    = "Allow"
    resources = ["*"]
  }

  statement {
    actions = [
      "athena:GetQueryExecution",
      "athena:GetQueryResults",
      "athena:StartQueryExecution"
    ]
    effect    = "Allow"
    resources = [aws_athena_workgroup.monitoring.arn]
  }

  statement {
    actions = [
      "athena:ListDatabases",
      "athena:ListTableMetadata"
    ]
    effect    = "Allow"
    resources = ["arn:aws:athena:*:*:datacatalog/AwsDataCatalog"]
  }

  statement {
    actions   = ["glue:GetDatabases"]
    effect    = "Allow"
    resources = ["arn:aws:glue:*:*:catalog"]
  }

  statement {
    actions = [
      "glue:GetPartition",
      "glue:GetPartitions",
      "glue:GetTable"
    ]
    effect = "Allow"
    resources = [
      "arn:aws:glue:*:*:catalog",
      "arn:aws:glue:*:*:database/${aws_athena_database.monitoring.name}",
      aws_glue_catalog_table.compute_jobs.arn
    ]
  }

  statement {
    actions = [
      "s3:GetBucketLocation",
      "s3:ListBucket",
      "s3:ListBucketMultipartUploads"
    ]
    effect = "Allow"
    resources = [
      aws_s3_bucket.monitoring.arn,
      aws_s3_bucket.monitoring_athena_results.arn,
    ]
  }

  statement {
    actions = [
      "s3:GetObject",
      "s3:ListMultipartUploadParts"
    ]
    effect    = "Allow"
    resources = ["${aws_s3_bucket.monitoring.arn}/*"]
  }

  statement {
    actions = [
      "s3:GetObject",
      "s3:ListMultipartUploadParts",
      "s3:PutObject"
    ]
    effect    = "Allow"
    resources = ["${aws_s3_bucket.monitoring_athena_results.arn}/*"]
  }
}

data "aws_iam_policy_document" "grafana_redshift_access" {
  statement {
    actions = [
      "redshift:DescribeClusters",
      "redshift-data:GetStatementResult",
      "redshift-data:DescribeStatement"
    ]
    effect    = "Allow"
    resources = ["*"]
  }

  statement {
    actions = [
      "redshift-data:DescribeTable",
      "redshift-data:ExecuteStatement",
      "redshift-data:ListTables",
      "redshift-data:ListSchemas"
    ]
    effect    = "Allow"
    resources = ["arn:aws:redshift:*:*:cluster:observes"]
  }

  statement {
    actions = ["redshift:GetClusterCredentials"]
    effect  = "Allow"
    resources = [
      "arn:aws:redshift:*:*:dbname:observes/observes",
      "arn:aws:redshift:*:*:dbuser:observes/fluiduser"
    ]
  }
}

data "aws_iam_policy_document" "grafana_prometheus_access" {
  statement {
    actions   = ["aps:ListWorkspaces"]
    effect    = "Allow"
    resources = ["*"]
  }

  statement {
    actions = [
      "aps:DescribeWorkspace",
      "aps:QueryMetrics",
      "aps:GetLabels",
      "aps:GetSeries",
      "aps:GetMetricMetadata"
    ]
    effect    = "Allow"
    resources = [aws_prometheus_workspace.monitoring.arn]
  }
}

data "aws_iam_policy_document" "grafana_xray_access" {
  statement {
    actions = [
      "xray:BatchGetTraces",
      "xray:GetTraceSummaries",
      "xray:GetTraceGraph",
      "xray:GetGroups",
      "xray:GetTimeSeriesServiceStatistics",
      "xray:GetInsightSummaries",
      "xray:GetInsight",
      "ec2:DescribeRegions"
    ]
    effect    = "Allow"
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "grafana" {
  source_policy_documents = [
    data.aws_iam_policy_document.grafana_athena_access.json,
    data.aws_iam_policy_document.grafana_redshift_access.json,
    data.aws_iam_policy_document.grafana_prometheus_access.json,
    data.aws_iam_policy_document.grafana_xray_access.json
  ]
}

resource "aws_iam_role" "grafana" {
  name               = "common-monitoring-grafana"
  assume_role_policy = data.aws_iam_policy_document.grafana_sts.json
}

resource "aws_iam_policy" "grafana" {
  name   = "common-monitoring-grafana"
  policy = data.aws_iam_policy_document.grafana.json
}

resource "aws_iam_role_policy_attachment" "grafana" {
  role       = aws_iam_role.grafana.name
  policy_arn = aws_iam_policy.grafana.arn
}

resource "okta_app_saml" "grafana" {
  label             = "Grafana - Universe"
  preconfigured_app = "amazonmanagedgrafanasaml"

  app_settings_json = jsonencode({
    "nameSpace" = "g-41cb062f0f"
    "region"    = "us-east-1"
  })
  app_links_json = jsonencode({
    "amazonmanagedgrafanasaml_link" = true,
  })
  user_name_template      = "$${source.login}"
  user_name_template_type = "BUILT_IN"

  attribute_statements {
    type   = "EXPRESSION"
    name   = "role"
    values = ["admin"]
  }

  lifecycle {
    ignore_changes = [users]
  }
}

resource "okta_app_user" "grafana_user_1" {
  app_id   = okta_app_saml.grafana.id
  user_id  = "00u3fmne3smuCPHVt357"
  username = "acuberos@fluidattacks.com"
}

resource "okta_app_user" "grafana_user_2" {
  app_id   = okta_app_saml.grafana.id
  user_id  = "00u1l65axaSd0IMke357"
  username = "jrestrepo@fluidattacks.com"
}

resource "okta_app_user" "grafana_user_3" {
  app_id   = okta_app_saml.grafana.id
  user_id  = "00u1la30aoz6g8iyD357"
  username = "dacevedo@fluidattacks.com"
}

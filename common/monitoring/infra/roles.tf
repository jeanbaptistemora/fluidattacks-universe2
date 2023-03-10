# Kinesis IAM role
data "aws_iam_policy_document" "kinesis_sts" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"

    principals {
      identifiers = ["events.amazonaws.com"]
      type        = "Service"
    }
  }
}

resource "aws_iam_role" "kinesis_stream" {
  name               = "monitoring-kinesis-stream"
  assume_role_policy = data.aws_iam_policy_document.kinesis_sts.json
}

data "aws_iam_policy_document" "kinesis_permissions" {
  statement {
    actions = [
      "kinesis:PutRecord",
      "kinesis:PutRecords",
    ]
    effect    = "Allow"
    resources = [aws_kinesis_stream.compute_jobs.arn]
  }
}

resource "aws_iam_policy" "kinesis_stream" {
  name   = "monitoring-kinesis-stream"
  policy = data.aws_iam_policy_document.kinesis_permissions.json
}

resource "aws_iam_role_policy_attachment" "kinesis_stream" {
  role       = aws_iam_role.kinesis_stream.name
  policy_arn = aws_iam_policy.kinesis_stream.arn
}

# Lambda IAM role
data "aws_iam_policy_document" "lambda_sts_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "lambda_role" {
  name               = "firehose_lambda_role"
  assume_role_policy = data.aws_iam_policy_document.lambda_sts_role.json
}

# Firehose IAM role
data "aws_iam_policy_document" "firehose_sts" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"

    principals {
      identifiers = ["firehose.amazonaws.com"]
      type        = "Service"
    }
  }
}

resource "aws_iam_role" "firehose_delivery" {
  name               = "common-monitoring-firehose-delivery"
  assume_role_policy = data.aws_iam_policy_document.firehose_sts.json
}

data "aws_iam_policy_document" "firehose_permissions" {
  statement {
    actions   = ["logs:PutLogEvents"]
    effect    = "Allow"
    resources = [aws_cloudwatch_log_stream.compute_jobs.arn]
  }

  statement {
    actions = [
      "kinesis:DescribeStream",
      "kinesis:GetShardIterator",
      "kinesis:GetRecords",
      "kinesis:ListShards",
    ]
    effect    = "Allow"
    resources = [aws_kinesis_stream.compute_jobs.arn]
  }

  statement {
    actions = [
      "lambda:GetFunctionConfiguration",
      "lambda:InvokeFunction",
    ]
    effect    = "Allow"
    resources = [aws_lambda_function.firehose_transform.arn]
  }

  statement {
    actions = [
      "s3:AbortMultipartUpload",
      "s3:GetBucketLocation",
      "s3:GetObject",
      "s3:ListBucket",
      "s3:ListBucketMultipartUploads",
      "s3:PutObject",
    ]
    effect = "Allow"
    resources = [
      "${aws_s3_bucket.monitoring.arn}",
      "${aws_s3_bucket.monitoring.arn}/*",
    ]
  }
}

resource "aws_iam_policy" "firehose_delivery" {
  name   = "common-monitoring-firehose-delivery"
  policy = data.aws_iam_policy_document.firehose_permissions.json
}

resource "aws_iam_role_policy_attachment" "firehose_delivery" {
  role       = aws_iam_role.firehose_delivery.name
  policy_arn = aws_iam_policy.firehose_delivery.arn
}

# Grafana IAM role
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

resource "aws_iam_role" "grafana" {
  name               = "common-monitoring-grafana"
  assume_role_policy = data.aws_iam_policy_document.grafana_sts.json
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

data "aws_iam_policy_document" "grafana_cloudwatch_access" {
  statement {
    actions = [
      "cloudwatch:DescribeAlarmsForMetric",
      "cloudwatch:DescribeAlarmHistory",
      "cloudwatch:DescribeAlarms",
      "cloudwatch:ListMetrics",
      "cloudwatch:GetMetricData",
      "cloudwatch:GetInsightRuleReport",
      "ec2:DescribeTags",
      "ec2:DescribeInstances",
      "ec2:DescribeRegions",
      "logs:DescribeLogGroups",
      "logs:GetLogGroupFields",
      "logs:StartQuery",
      "logs:StopQuery",
      "logs:GetQueryResults",
      "logs:GetLogEvents",
      "tag:GetResources"
    ]
    resources = ["*"]
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
      "xray:GetServiceGraph",
      "ec2:DescribeRegions"
    ]
    effect    = "Allow"
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "grafana" {
  source_policy_documents = [
    data.aws_iam_policy_document.grafana_athena_access.json,
    data.aws_iam_policy_document.grafana_cloudwatch_access.json,
    data.aws_iam_policy_document.grafana_redshift_access.json,
    data.aws_iam_policy_document.grafana_prometheus_access.json,
    data.aws_iam_policy_document.grafana_xray_access.json
  ]
}

resource "aws_iam_policy" "grafana" {
  name   = "common-monitoring-grafana"
  policy = data.aws_iam_policy_document.grafana.json
}

resource "aws_iam_role_policy_attachment" "grafana" {
  role       = aws_iam_role.grafana.name
  policy_arn = aws_iam_policy.grafana.arn
}

# Prometheus K8s-IAM role
data "aws_eks_cluster" "k8s_cluster" {
  name = "common-k8s"
}

data "aws_iam_policy_document" "k8s_oidc" {
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]

    condition {
      test     = "StringEquals"
      values   = ["system:serviceaccount:kube-system:${local.prometheus_role_name}"]
      variable = "${replace(data.aws_eks_cluster.k8s_cluster.identity[0].oidc[0].issuer, "https://", "")}:sub"
    }

    principals {
      type        = "Federated"
      identifiers = ["arn:aws:iam::${data.aws_caller_identity.main.account_id}:oidc-provider/${replace(data.aws_eks_cluster.k8s_cluster.identity[0].oidc[0].issuer, "https://", "")}"]
    }
  }
}

resource "aws_iam_role" "monitoring" {
  name               = local.prometheus_role_name
  assume_role_policy = data.aws_iam_policy_document.k8s_oidc.json
}

data "aws_iam_policy_document" "prometheus_permissions" {
  statement {
    actions = [
      "aps:GetLabels",
      "aps:GetMetricMetadata",
      "aps:GetSeries",
      "aps:RemoteWrite"
    ]
    resources = [
      aws_prometheus_workspace.monitoring.arn
    ]
  }
}

data "aws_iam_policy_document" "prometheus_xray_permissions" {
  statement {
    actions = [
      "xray:PutTelemetryRecords",
      "xray:PutTraceSegments"
    ]
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "monitoring_permissions" {
  source_policy_documents = [
    data.aws_iam_policy_document.prometheus_permissions.json,
    data.aws_iam_policy_document.prometheus_xray_permissions.json,
  ]
}

resource "aws_iam_policy" "monitoring" {
  name        = "EKSMonitoring"
  description = "Permissions required for ADOT Collector to send scraped metrics to AMP and traces to X-Ray"
  policy      = data.aws_iam_policy_document.monitoring_permissions.json
}

resource "aws_iam_role_policy_attachment" "prometheus_access" {
  role       = aws_iam_role.monitoring.name
  policy_arn = aws_iam_policy.monitoring.arn
}

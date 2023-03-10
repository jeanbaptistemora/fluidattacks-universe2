# Bucket where all the state changes events from Batch will be stored
resource "aws_s3_bucket" "monitoring" {
  bucket = "common-monitoring"

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "monitoring" {
  bucket = aws_s3_bucket.monitoring.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_acl" "bucket_acl" {
  bucket = aws_s3_bucket.monitoring.id
  acl    = "private"
}

# Bucket where all the Athena query results will be stored
resource "aws_s3_bucket" "monitoring_athena_results" {
  bucket = "common-monitoring-athena-results"
}

resource "aws_s3_bucket_lifecycle_configuration" "monitoring_athena_results" {
  bucket = aws_s3_bucket.monitoring_athena_results.id

  rule {
    id     = "remove old ${aws_s3_bucket.monitoring_athena_results.id} objects"
    status = "Enabled"

    expiration {
      days = 1
    }
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "monitoring_athena_results" {
  bucket = aws_s3_bucket.monitoring_athena_results.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

# Athena DB setup
resource "aws_athena_database" "monitoring" {
  name   = "common_monitoring"
  bucket = aws_s3_bucket.monitoring_athena_results.bucket
}

resource "aws_athena_workgroup" "monitoring" {
  name = "common-monitoring"

  configuration {
    result_configuration {
      output_location = "s3://${aws_s3_bucket.monitoring_athena_results.bucket}/"
    }
  }
}

# Glue DB schema
resource "aws_glue_catalog_table" "compute_jobs" {
  database_name = aws_athena_database.monitoring.name
  name          = "compute_jobs"

  table_type = "EXTERNAL_TABLE"

  storage_descriptor {
    location      = "s3://${aws_s3_bucket.monitoring.bucket}/compute-jobs"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat"

    ser_de_info {
      serialization_library = "org.openx.data.jsonserde.JsonSerDe"
      parameters = {
        "serialization.format" = 1
      }
    }

    sort_columns {
      column     = "time"
      sort_order = 0
    }

    columns {
      name = "detail"
      type = replace(
        <<-EOF
          struct<
            container:struct<
              command:array<string>,
              environment:array<struct<name:string>>,
              exitCode:bigint,
              image:string,
              logStreamName:string,
              memory:bigint,
              resourceRequirements:array<struct<type:string, value:string>>,
              vcpus:bigint
            >,
            createdAt:timestamp,
            jobId:string,
            jobName:string,
            jobQueue:string,
            startedAt:timestamp,
            status:string,
            statusReason:string,
            stoppedAt:timestamp
          >
        EOF
        ,
      "/[\n ]+/", "")
    }

    columns {
      name = "id"
      type = "string"
    }

    columns {
      name = "time"
      type = "timestamp"
    }
  }
}

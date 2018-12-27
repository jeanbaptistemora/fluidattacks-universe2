  # AWS vars
variable "dynamo_access_key" {}
variable "dynamo_secret_key" {}
variable "region" {}

provider "aws" {
  access_key = "${var.dynamo_access_key}"
  secret_key = "${var.dynamo_secret_key}"
  region = "${var.region}"
}

resource "aws_dynamodb_table" "alerts_by_company" {
  name           = "FI_alerts_by_company"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "company_name"
  range_key      = "project_name"

  attribute {
    name = "company_name"
    type = "S"
  }

  attribute {
    name = "project_name"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "comments" {
  name           = "FI_comments"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = "finding_id"
  range_key      = "user_id"

  attribute {
    name = "finding_id"
    type = "N"
  }

  attribute {
    name = "user_id"
    type = "N"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "project_comments" {
  name           = "fi_project_comments"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "project_name"
  range_key      = "user_id"

  attribute {
    name = "project_name"
    type = "S"
  }

  attribute {
    name = "user_id"
    type = "N"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "events" {
  name           = "fi_events"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "event_id"

  attribute {
    name = "event_id"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}


resource "aws_dynamodb_table" "findings_email" {
  name           = "FI_findings_email"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "project_name"
  range_key      = "unique_id"

  attribute {
    name = "project_name"
    type = "S"
  }

  attribute {
    name = "unique_id"
    type = "N"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "remediated" {
  name           = "FI_remediated"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "finding_id"

  attribute {
    name = "finding_id"
    type = "N"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "toe" {
  name           = "FI_toe"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "project"

  attribute {
    name = "project"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "weekly_report" {
  name           = "FI_weekly_report"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "init_date"

  attribute {
    name = "init_date"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}
resource "aws_dynamodb_table" "projects" {
  name           = "FI_projects"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "project_name"

  attribute {
    name = "project_name"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}
resource "aws_dynamodb_table" "users" {
  name           = "FI_users"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "email"

  attribute {
    name = "email"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}
resource "aws_dynamodb_table" "project_access" {
  name           = "FI_project_access"
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "user_email"
  range_key      = "project_name"

  attribute {
    name = "user_email"
    type = "S"
  }

  attribute {
    name = "project_name"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "findings" {
  name           = "FI_findings"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = "finding_id"

  attribute {
    name = "finding_id"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_dynamodb_table" "vulnerabilities" {
  name           = "FI_vulnerabilities"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = "finding_id"
  range_key      = "UUID"

  attribute {
    name = "finding_id"
    type = "S"
  }

  attribute {
    name = "UUID"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }
}

resource "aws_appautoscaling_target" "dynamodb_table_read_target" {
  max_capacity       = 10
  min_capacity       = 2
  resource_id        = "table/FI_comments"
  scalable_dimension = "dynamodb:table:ReadCapacityUnits"
  service_namespace  = "dynamodb"
}

resource "aws_appautoscaling_policy" "dynamodb_table_read_policy" {
  name               = "DynamoDBReadCapacityUtilization:${aws_appautoscaling_target.dynamodb_table_read_target.resource_id}"
  policy_type        = "TargetTrackingScaling"
  resource_id        = "${aws_appautoscaling_target.dynamodb_table_read_target.resource_id}"
  scalable_dimension = "${aws_appautoscaling_target.dynamodb_table_read_target.scalable_dimension}"
  service_namespace  = "${aws_appautoscaling_target.dynamodb_table_read_target.service_namespace}"

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "DynamoDBReadCapacityUtilization"
    }
    target_value = 70
  }
}

resource "aws_appautoscaling_target" "dynamodb_table_write_target" {
  max_capacity       = 10
  min_capacity       = 2
  resource_id        = "table/FI_comments"
  scalable_dimension = "dynamodb:table:WriteCapacityUnits"
  service_namespace  = "dynamodb"
}

resource "aws_appautoscaling_policy" "dynamodb_table_write_policy" {
  name               = "DynamoDBWriteCapacityUtilization:${aws_appautoscaling_target.dynamodb_table_write_target.resource_id}"
  policy_type        = "TargetTrackingScaling"
  resource_id        = "${aws_appautoscaling_target.dynamodb_table_write_target.resource_id}"
  scalable_dimension = "${aws_appautoscaling_target.dynamodb_table_write_target.scalable_dimension}"
  service_namespace  = "${aws_appautoscaling_target.dynamodb_table_write_target.service_namespace}"

  target_tracking_scaling_policy_configuration {
    predefined_metric_specification {
      predefined_metric_type = "DynamoDBWriteCapacityUtilization"
    }
    target_value = 70
  }
}

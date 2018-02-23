provider "aws" {
    region = "us-east-1"
}

resource "aws_dynamodb_table" "comments" {
  name           = "comments"
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
}

resource "aws_dynamodb_table" "remediated" {
  name           = "remediated"
  read_capacity  = 10
  write_capacity = 10
  hash_key       = "finding_id"
  
  attribute {
    name = "finding_id"
    type = "N"
  }
}

resource "aws_dynamodb_table" "toe" {
  name           = "toe"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "project"

  attribute {
    name = "project"
    type = "S"
  }  
}

resource "aws_dynamodb_table" "findings" {
  name           = "findings"
  read_capacity  = 5
  write_capacity = 5
  hash_key       = "finding_id"
  
  attribute {
    name = "finding_id"
    type = "N"
  }
}
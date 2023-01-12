resource "aws_iam_role" "firehose_delivery" {
  name = "common-monitoring-firehose-delivery"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : "sts:AssumeRole",
        "Principal" : {
          "Service" : "firehose.amazonaws.com"
        },
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "firehose_delivery" {
  role       = aws_iam_role.firehose_delivery.name
  policy_arn = aws_iam_policy.firehose_delivery.arn
}

resource "aws_iam_policy" "firehose_delivery" {
  name = "common-monitoring-firehose-delivery"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "logs:PutLogEvents"
        ],
        "Resource" : [
          aws_cloudwatch_log_stream.compute_jobs.arn,
        ]
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "kinesis:DescribeStream",
          "kinesis:GetShardIterator",
          "kinesis:GetRecords",
          "kinesis:ListShards"
        ],
        "Resource" : [
          aws_kinesis_stream.compute_jobs.arn
        ]
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "lambda:GetFunctionConfiguration",
          "lambda:InvokeFunction"
        ],
        "Resource" : [
          aws_lambda_function.firehose_transform.arn
        ]
      },
      {
        "Effect" : "Allow",
        "Action" : [
          "s3:AbortMultipartUpload",
          "s3:GetBucketLocation",
          "s3:GetObject",
          "s3:ListBucket",
          "s3:ListBucketMultipartUploads",
          "s3:PutObject"
        ],
        "Resource" : [
          "${aws_s3_bucket.monitoring.arn}",
          "${aws_s3_bucket.monitoring.arn}/*",
        ],
      },
    ]
  })
}

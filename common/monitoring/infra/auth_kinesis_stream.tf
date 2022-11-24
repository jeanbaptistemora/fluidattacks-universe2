resource "aws_iam_role" "kinesis_stream" {
  name = "monitoring-kinesis-stream"

  assume_role_policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : "sts:AssumeRole",
        "Principal" : {
          "Service" : "events.amazonaws.com"
        },
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "kinesis_stream" {
  role       = aws_iam_role.kinesis_stream.name
  policy_arn = aws_iam_policy.kinesis_stream.arn
}

resource "aws_iam_policy" "kinesis_stream" {
  name = "monitoring-kinesis-stream"

  policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "kinesis:PutRecord",
          "kinesis:PutRecords",
        ],
        "Resource" : [
          aws_kinesis_stream.compute_jobs.arn
        ],
      },
    ]
  })
}

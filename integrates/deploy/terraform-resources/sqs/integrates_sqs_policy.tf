resource "aws_sqs_queue_policy" "integrates-queue-policy" {
  queue_url = aws_sqs_queue.integrates-queue.id
  policy    = <<POLICY
{
  "Version": "2012-10-17",
  "Id": "integrates-queue-policy",
  "Statement": [
    {
      "Sid": "First",
      "Effect": "Allow",
      "Principal": "*",
      "Action": [
        "SQS:SendMessage",
        "SQS:DeleteMessage",
        "SQS:GetQueueAttributes",
        "SQS:ReceiveMessage"
      ],
     "Resource": "${aws_sqs_queue.integrates-queue.arn}"
    }
  ]
}
POLICY
}

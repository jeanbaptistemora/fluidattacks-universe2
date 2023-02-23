resource "aws_kinesis_stream" "observes_mirror" {
  name             = "observes-mirror"
  retention_period = 24

  stream_mode_details {
    stream_mode = "ON_DEMAND"
  }

  lifecycle {
    prevent_destroy = true
  }
}

resource "aws_cloudwatch_metric_alarm" "fs-cpu-usage" {
  alarm_name                = "FS_CPU_USAGE"
  comparison_operator       = "GreaterThanThreshold"
  evaluation_periods        = "3"
  metric_name               = "CPUUtilization"
  namespace                 = "AWS/EC2"
  period                    = "120"
  statistic                 = "Average"
  threshold                 = "80"
  alarm_description         = "This metric monitors ec2 cpu utilization"
  datapoints_to_alarm       = "3"
  treat_missing_data        = "breaching"
  dimensions {
    InstanceId = "${aws_instance.fluidserves.id}"
  }
}

resource "aws_cloudwatch_metric_alarm" "fs-disk-usage" {
  alarm_name                = "FS_DISK_USAGE"
  comparison_operator       = "GreaterThanThreshold"
  evaluation_periods        = "3"
  metric_name               = "disk_used_percent"
  namespace                 = "CWAgent"
  period                    = "120"
  statistic                 = "Average"
  threshold                 = "80"
  alarm_description         = "This metric monitors ec2 disk utilization"
  datapoints_to_alarm       = "3"
  treat_missing_data        = "notBreaching"
  dimensions {
    InstanceId = "${aws_instance.fluidserves.id}"
  }
}
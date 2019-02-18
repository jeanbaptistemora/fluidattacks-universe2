data "aws_iam_policy_document" "ecs_role" {
  version         = "2012-10-17"
  statement {
    sid           = ""
    effect        = "Allow"
    actions       = [
      "sts:AssumeRole",
    ]
    principals    = {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}
data "aws_iam_policy_document" "ecs_instance_role_policy" {
  version         = "2012-10-17"
  statement {
    effect        = "Allow"
    actions       = [
      "ecs:CreateCluster",
      "ecs:DeregisterContainerInstance",
      "ecs:DiscoverPollEndpoint",
      "ecs:Poll",
      "ecs:RegisterContainerInstance",
      "ecs:StartTelemetrySession",
      "ecs:Submit*",
      "ecs:StartTask",
    ]
    resources     = [
      "*"
    ]
  }
}
data "aws_iam_policy_document" "ecs_service_role_policy" {
  version         = "2012-10-17"
  statement {
    effect        = "Allow"
    actions       = [
      "elasticloadbalancing:Describe*",
      "elasticloadbalancing:DeregisterTargets",
      "elasticloadbalancing:RegisterTargets",
      "ec2:Describe*",
      "ec2:AuthorizeSecurityGroupIngress",
    ]
    resources     = [
      "*"
    ]
  }
}
resource "aws_iam_instance_profile" "ecs_instance_profile" {
  name = "${var.name_prefix}_ecs_instance_profile"
  role = "${aws_iam_role.ecs_instance_role.name}"
}
resource "aws_iam_role" "ecs_instance_role" {
  name = "${var.name_prefix}_ecs_instance_role"
  assume_role_policy = "${data.aws_iam_policy_document.ecs_role.json}"
}
resource "aws_iam_role" "ecs_service_role" {
  name = "${var.name_prefix}_ecs_service_role"
  assume_role_policy = "${data.aws_iam_policy_document.ecs_role.json}"
}
resource "aws_iam_role_policy" "ecs_instance_role_policy" {
  name = "${var.name_prefix}_ecs_instance_role_policy"
  role = "${aws_iam_role.ecs_instance_role.id}"
  policy = "${data.aws_iam_policy_document.ecs_instance_role_policy.json}"
}
resource "aws_iam_role_policy" "ecs_service_role_policy" {
  name = "${var.name_prefix}_ecs_service_role"
  role = "${aws_iam_role.ecs_service_role.id}"
  policy = "${data.aws_iam_policy_document.ecs_service_role_policy.json}"
}

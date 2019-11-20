resource "aws_security_group" "autoscaling_ci_security_group" {
  name        = "AutoscalingCISecurityGroup"
  description = "Allow communication between GitLab, bastion and processing machines"
  vpc_id      = var.autostaling_ci_vpc_id

  ingress {
    description = "ssh-access"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = []
    self        = true
  }

  ingress {
    description = "docker-access"
    from_port   = 2376
    to_port     = 2376
    protocol    = "tcp"
    cidr_blocks = []
    self        = true
  }

  egress {
    description = "default-aws-egress-rule"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

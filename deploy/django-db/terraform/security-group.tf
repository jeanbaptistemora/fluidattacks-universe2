resource "aws_security_group" "django-db" {
  name        = "django-db"
  description = "Security group for Integrates django-db"
  vpc_id      = var.fluid-vpc-id

  ingress {
    description = "ssh-access"
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
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

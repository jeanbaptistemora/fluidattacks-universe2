resource "aws_lb_target_group" "ip-example" {
  name        = "tf-example-lb-tg"
  protocol    = "HTTP"
  target_type = "lambda"
  vpc_id      = aws_vpc.main.id
}

resource "aws_lb_target_group" "ip-example" {
  name        = "tf-example-lb-tg"
  protocol    = "HTTP"
  target_type = "ip"
  vpc_id      = aws_vpc.main.id
}

resource "aws_lb_target_group" "ip-example" {
  name     = "tf-example-lb-tg"
  protocol = "HTTP"
  vpc_id   = aws_vpc.main.id
}

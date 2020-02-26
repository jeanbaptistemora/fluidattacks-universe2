resource "aws_subnet" "region-a" {
  vpc_id            = var.fluid-vpc-id
  availability_zone = "${var.region}a"
  cidr_block        = "192.168.4.0/25"
}

resource "aws_subnet" "region-b" {
  vpc_id            = var.fluid-vpc-id
  availability_zone = "${var.region}b"
  cidr_block        = "192.168.4.128/25"
}

resource "aws_db_subnet_group" "django-db" {
  name       = "django-db"
  subnet_ids = [
    aws_subnet.region-a.id,
    aws_subnet.region-b.id,
  ]
}

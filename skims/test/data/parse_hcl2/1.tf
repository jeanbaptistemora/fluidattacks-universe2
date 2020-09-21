# Comment

module "iam_user" {
  source = "modules\/iam-user"

  name = "${var.iamuser}"
  force_destroy = true

  tags = {
    proyecto = "${var.proyecto}",
    analista = "${var.analista}"
  }
}

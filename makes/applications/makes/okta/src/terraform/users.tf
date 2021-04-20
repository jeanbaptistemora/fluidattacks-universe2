resource "okta_user" "dsalazar" {
  email      = "dsalazar@fluidattacks.com"
  first_name = "Daniel"
  last_name  = "Salazar"
  login      = "dsalazar@fluidattacks.com"
  admin_roles = [
    "SUPER_ADMIN",
  ]
}

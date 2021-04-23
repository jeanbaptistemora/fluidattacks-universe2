resource "okta_user" "users" {
  for_each    = { for user in jsondecode(var.okta_users) : user.id => user }
  email       = each.value.email
  first_name  = each.value.first_name
  last_name   = each.value.last_name
  login       = each.value.email
  admin_roles = each.value.admin_roles
}

locals {
  keys = {
    prod_airs = {
      admins = [
        "prod_makes",
      ]
      users = [
        "prod_airs",
      ]
      tags = {
        "Name"               = "prod_airs"
        "management:area"    = "cost"
        "management:product" = "makes"
        "management:type"    = "product"
      }
    }
  }
}

module "keys" {
  source   = "../../../modules/key"
  for_each = local.keys

  name   = each.key
  admins = each.value.admins
  users  = each.value.users
  tags   = each.value.tags
}

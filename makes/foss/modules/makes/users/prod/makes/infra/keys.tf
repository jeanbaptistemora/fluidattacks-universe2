locals {
  keys = {
    prod_makes = {
      admins = [
        "prod_makes",
      ]
      users = []
      tags = {
        "Name"               = "prod_makes"
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

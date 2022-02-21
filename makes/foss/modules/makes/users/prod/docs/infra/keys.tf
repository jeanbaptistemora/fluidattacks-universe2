locals {
  keys = {
    prod_docs = {
      admins = [
        "prod_makes",
      ]
      users = [
        "prod_docs",
      ]
      tags = {
        "Name"               = "prod_docs"
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

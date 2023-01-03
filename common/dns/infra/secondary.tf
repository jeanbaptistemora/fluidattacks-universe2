module "secondary_domains" {
  source = "./modules/secondary-domain"

  for_each = toset(
    [
      "fluid.com.co",
      "fluid.la",
      "fluidattacks.co",
      "fluidattacks.com.co",
      "fluidattacks.net",
      "fluidsignal.co",
      "fluidsignal.com",
      "fluidsignal.com.co",
    ]
  )

  domain = each.key
}

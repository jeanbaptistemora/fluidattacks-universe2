module "secondary_domains" {
  source = "./modules/secondary-domain"

  for_each = toset(
    [
      "atfluid.com",
      "fluid.com.co",
      "fluid.la",
      "fluidattacks.app",
      "fluidattacks.co",
      "fluidattacks.com.co",
      "fluidattacks.info",
      "fluidattacks.io",
      "fluidattacks.net",
      "fluidattacks.org",
      "fluidattacks.website",
      "fluidsignal.co",
      "fluidsignal.com",
      "fluidsignal.com.co",
    ]
  )

  domain = each.key
}

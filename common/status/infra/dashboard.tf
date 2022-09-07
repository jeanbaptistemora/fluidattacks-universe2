# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

resource "checkly_dashboard" "main" {
  custom_url      = "fluidattacks"
  custom_domain   = "status.fluidattacks.com"
  logo            = "https://res.cloudinary.com/fluid-attacks/image/upload/q_auto,f_auto/v1619554789/airs/logo-fluid-attacks-light_lsckin.webp"
  header          = "Status Page"
  refresh_rate    = 60
  paginate        = true
  pagination_rate = 60
  hide_tags       = true
  width           = "FULL"

  tags = [
    "production",
  ]
}

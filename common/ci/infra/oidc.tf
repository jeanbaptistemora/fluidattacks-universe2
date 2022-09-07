# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

data "tls_certificate" "main" {
  url = "https://gitlab.com/.well-known/openid-configuration"
}

resource "aws_iam_openid_connect_provider" "main" {
  url             = "https://gitlab.com"
  client_id_list  = ["https://gitlab.com"]
  thumbprint_list = data.tls_certificate.main.certificates[*].sha1_fingerprint
}

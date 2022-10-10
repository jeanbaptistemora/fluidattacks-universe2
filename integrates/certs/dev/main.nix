# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{makeSslCertificate, ...}:
makeSslCertificate {
  name = "integrates-certs-development";
  options = [
    [
      "-subj"
      (builtins.concatStringsSep "" [
        "/C=CO"
        "/CN=fluidattacks.com"
        "/emailAddress=development@fluidattacks.com"
        "/L=Medellin"
        "/O=Fluid Attacks"
        "/ST=Antioquia"
      ])
    ]
  ];
}

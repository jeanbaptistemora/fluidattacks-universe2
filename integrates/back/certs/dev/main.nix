# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{makeSslCertificate, ...}:
makeSslCertificate {
  name = "integrates-back-certs-development";
  options = [
    ["-subj" "/C=CO"]
    ["-subj" "/CN=fluidattacks.com"]
    ["-subj" "/emailAddress=development@fluidattacks.com"]
    ["-subj" "/L=Medellin"]
    ["-subj" "/O=Fluid"]
    ["-subj" "/ST=Antioquia"]
  ];
}

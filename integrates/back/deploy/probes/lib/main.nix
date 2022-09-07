# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeTemplate,
  ...
}:
makeTemplate {
  name = "integrates-back-probes-lib";
  searchPaths.bin = [
    inputs.nixpkgs.awscli
    inputs.nixpkgs.curl
    inputs.nixpkgs.gnugrep
  ];
  template = ./template.sh;
}

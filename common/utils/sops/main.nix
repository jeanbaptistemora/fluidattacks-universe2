# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeTemplate,
  ...
}:
makeTemplate {
  searchPaths = {
    bin = [
      inputs.nixpkgs.gnugrep
      inputs.nixpkgs.jq
      inputs.nixpkgs.sops
    ];
  };
  name = "utils-bash-lib-sops";
  template = ./template.sh;
}

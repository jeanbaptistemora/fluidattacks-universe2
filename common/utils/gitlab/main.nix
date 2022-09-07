# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeTemplate,
  ...
}:
makeTemplate {
  name = "utils-gitlab";
  searchPaths = {
    bin = [
      inputs.nixpkgs.curl
      inputs.nixpkgs.jq
    ];
  };
  template = ./template.sh;
}

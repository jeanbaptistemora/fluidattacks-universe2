# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeTemplate,
  makeTerraformEnvironment,
  ...
}:
makeTemplate {
  searchPaths = {
    bin = [
      inputs.nixpkgs.gnugrep
    ];
    source = [
      (makeTerraformEnvironment {
        version = "1.0";
      })
    ];
  };
  name = "common-storage-lib";
  template = ./template.sh;
}

# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeTemplate,
  outputs,
  ...
}:
makeTemplate {
  searchPaths = {
    bin = [
      inputs.nixpkgs.awscli
      inputs.nixpkgs.jq
    ];
    source = [
      outputs."/common/utils/env"
    ];
  };
  name = "utils-bash-lib-aws";
  template = ./template.sh;
}

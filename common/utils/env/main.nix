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
  name = "utils-env";
  searchPaths = {
    bin = [
      inputs.nixpkgs.curl
      inputs.nixpkgs.jq
    ];
    source = [
      outputs."/common/utils/gitlab"
      outputs."/common/utils/common"
    ];
  };
  template = ./template.sh;
}

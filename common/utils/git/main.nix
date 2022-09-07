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
  replace = {
    __argGit__ = "${inputs.nixpkgs.git}/bin/git";
  };
  name = "utils-bash-lib-git";
  searchPaths = {
    bin = [
      inputs.nixpkgs.git
    ];
    source = [
      outputs."/common/utils/env"
    ];
  };
  template = ./template.sh;
}

# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeNodeJsVersion,
  makeScript,
  outputs,
  ...
}:
makeScript {
  name = "docs";
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.xdg_utils
      outputs."/docs/generate/criteria"
      (makeNodeJsVersion "16")
    ];
  };
  entrypoint = ./entrypoint.sh;
}

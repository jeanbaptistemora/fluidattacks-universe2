# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  ...
}:
makeScript {
  name = "common-kill-tree";
  searchPaths = {
    bin = [
      inputs.nixpkgs.procps
    ];
  };
  entrypoint = ./entrypoint.sh;
}

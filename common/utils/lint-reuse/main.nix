# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  projectPath,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "lint-reuse";
  replace = {
    __argProjectPath__ = projectPath "/";
  };
  searchPaths.bin = [inputs.nixpkgs.reuse];
}

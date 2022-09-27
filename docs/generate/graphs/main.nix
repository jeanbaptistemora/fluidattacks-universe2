# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  ...
}:
makeScript {
  name = "docs-generate-graphs";
  aliases = ["generate-graphs"];
  entrypoint = ./entrypoint.sh;
  searchPaths.bin = [
    inputs.nixpkgs.findutils
    inputs.nixpkgs.graphviz
  ];
}

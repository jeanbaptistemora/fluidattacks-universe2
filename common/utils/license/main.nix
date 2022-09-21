# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "license";
  searchPaths.bin = [
    inputs.nixpkgs.coreutils
    inputs.nixpkgs.gawk
    inputs.nixpkgs.reuse
    inputs.nixpkgs.gnused
    inputs.nixpkgs.gnugrep
    inputs.nixpkgs.git
  ];
}

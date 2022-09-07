# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  managePorts,
  ...
}:
makeScript {
  name = "integrates-cache";
  searchPaths = {
    bin = [
      inputs.nixpkgs.redis
    ];
    source = [
      managePorts
    ];
  };
  entrypoint = ./entrypoint.sh;
}

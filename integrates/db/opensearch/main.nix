# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  managePorts,
  outputs,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "opensearch";
  replace = {
    __argOpensearch__ = outputs."/integrates/db/opensearch/pkg";
  };
  searchPaths = {
    bin = [inputs.nixpkgs.jdk11_headless];
    source = [managePorts];
  };
}

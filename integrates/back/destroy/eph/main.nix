# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  searchPaths = {
    bin = [inputs.nixpkgs.kubectl];
    kubeConfig = [".kubernetes"];
    source = [outputs."/common/utils/aws"];
  };
  name = "integrates-back-destroy-eph";
  entrypoint = ./entrypoint.sh;
}

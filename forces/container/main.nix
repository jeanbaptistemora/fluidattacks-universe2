# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeContainerImage,
  makeDerivation,
  outputs,
  ...
}:
makeContainerImage {
  config.WorkingDir = "/src";
  layers = [
    inputs.nixpkgs.bash
    inputs.nixpkgs.coreutils
    outputs."/forces"
    (makeDerivation {
      builder = ./builder.sh;
      name = "forces-oci-build-customization-layer";
    })
  ];
}

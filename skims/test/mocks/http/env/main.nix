# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeSearchPaths,
  managePorts,
  ...
}:
makeSearchPaths {
  bin = [
    inputs.nixpkgs.python38Packages.flask
  ];
  source = [
    managePorts
  ];
  pythonPackage38 = [
    inputs.nixpkgs.python38Packages.flask
  ];
}

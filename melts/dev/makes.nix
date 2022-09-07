# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  makeSearchPaths,
  outputs,
  ...
}: {
  dev = {
    melts = {
      source = [
        outputs."/melts/config/development"
        outputs."/melts/config/runtime"
        (makeSearchPaths {
          pythonPackage = ["$PWD/melts"];
        })
      ];
    };
  };
}

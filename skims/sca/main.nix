# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  inputs,
  makeScript,
  outputs,
  projectPath,
  ...
}:
makeScript {
  name = "skims-sca-update";
  searchPaths = {
    pythonMypy = [
      (projectPath "/skims/sca/update")
    ];
    bin = [
      inputs.nixpkgs.python38
      outputs."/skims"
    ];
    pythonPackage = [
      (projectPath "/skims/sca/update")
    ];
    source = [
      outputs."/skims/config/runtime"
    ];
  };

  replace = {
    __argUpdateSCA__ = "sca/update/__init__.py";
  };

  entrypoint = ./entrypoint.sh;
}

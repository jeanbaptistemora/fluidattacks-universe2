# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  pythonPkgs,
}:
lib.buildPythonPackage rec {
  pname = "returns";
  version = "0.19.0";
  src = lib.fetchPypi {
    inherit pname version;
    sha256 = "RUS7Z4ScHvG794I3WdQzp3OVnlt3qP0G0B/vbQYPKsU=";
  };
  doCheck = false;
  propagatedBuildInputs = [pythonPkgs.typing-extensions];
}

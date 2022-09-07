# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  python_pkgs,
}:
lib.buildPythonPackage rec {
  pname = "grimp";
  version = "1.2.3";
  src = lib.fetchPypi {
    inherit pname version;
    sha256 = "v+4uMpCESktuAI9nwH2rVPOHA/wL8BYRGaVHMbob7Q0=";
  };
  pythonImportsCheck = [pname];
  checkInputs = with python_pkgs; [pytestCheckHook pyyaml];
  propagatedBuildInputs = with python_pkgs; [networkx];
}

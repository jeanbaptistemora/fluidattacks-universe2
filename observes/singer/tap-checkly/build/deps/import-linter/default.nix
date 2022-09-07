# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  lib,
  pythonPkgs,
}: let
  grimp = lib.buildPythonPackage rec {
    pname = "grimp";
    version = "1.2.3";
    src = lib.fetchPypi {
      inherit pname version;
      hash = "sha256:v+4uMpCESktuAI9nwH2rVPOHA/wL8BYRGaVHMbob7Q0=";
    };
    doCheck = false;
    propagatedBuildInputs = [pythonPkgs.networkx];
  };
in
  lib.buildPythonPackage rec {
    pname = "import-linter";
    version = "1.2.6";
    src = lib.fetchPypi {
      inherit pname version;
      hash = "sha256:0fjUy8CnuzAwt3ONfi6tz/kY8HCp2wUiuV3yqINNR94=";
    };
    propagatedBuildInputs = [grimp pythonPkgs.click];
  }

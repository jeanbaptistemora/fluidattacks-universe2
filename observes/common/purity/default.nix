# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  legacyPkgs,
  pythonVersion,
  src,
  system,
}: let
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).tool.poetry;
  lib = {
    buildEnv = legacyPkgs."${pythonVersion}".buildEnv.override;
    buildPythonPackage = legacyPkgs."${pythonVersion}".pkgs.buildPythonPackage;
    fetchPypi = legacyPkgs.python3Packages.fetchPypi;
  };
  python_pkgs = import ./build/deps {
    inherit lib system pythonVersion legacyPkgs;
    pythonPkgs = legacyPkgs."${pythonVersion}Packages";
  };
  self_pkgs = import ./build/pkg {
    inherit src lib metadata python_pkgs;
  };
in
  self_pkgs

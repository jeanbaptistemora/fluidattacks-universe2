# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  extras,
  legacyPkgs,
  pythonVersion,
  src,
}: let
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).tool.poetry;
  lib = {
    buildEnv = legacyPkgs."${pythonVersion}".buildEnv.override;
    buildPythonPackage = legacyPkgs."${pythonVersion}".pkgs.buildPythonPackage;
    fetchPypi = legacyPkgs.python3Packages.fetchPypi;
  };
  pythonPkgs = import ./build/deps {
    inherit extras legacyPkgs lib pythonVersion;
  };
  self_pkgs = import ./build/pkg {
    inherit src lib metadata pythonPkgs;
  };
  checks = import ./check {self_pkg = self_pkgs.pkg;};
in
  self_pkgs // {check = checks;}

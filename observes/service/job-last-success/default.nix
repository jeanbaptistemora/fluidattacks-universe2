# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  local_pkgs,
  pkgs,
  python_version,
  src,
}: let
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).tool.poetry;
  lib = {
    buildEnv = pkgs."${python_version}".buildEnv.override;
    buildPythonPackage = pkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = pkgs.python3Packages.fetchPypi;
  };
  python_pkgs = import ./build/deps {
    inherit local_pkgs pkgs lib python_version;
  };
  self_pkgs = import ./build/pkg {
    inherit src lib metadata python_pkgs;
  };
  checks = import ./check {self_pkg = self_pkgs.pkg;};
in
  self_pkgs // {check = checks;}

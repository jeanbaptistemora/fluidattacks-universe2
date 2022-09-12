# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
{
  local_pkgs,
  pkgs,
  python_version,
  src,
}: let
  metadata = let
    _metadata = (builtins.fromTOML (builtins.readFile ./pyproject.toml)).project;
    file_str = builtins.readFile "${src}/${_metadata.name}/__init__.py";
    match = builtins.match ".*__version__ *= *\"(.+?)\"\n.*" file_str;
    version = builtins.elemAt match 0;
  in
    _metadata // {inherit version;};
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
in
  self_pkgs

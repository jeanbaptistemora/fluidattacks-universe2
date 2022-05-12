{
  system,
  legacy_pkgs,
  local_lib,
  src,
}: let
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).tool.poetry;
  lib = {
    buildEnv = legacy_pkgs.python39.buildEnv.override;
    buildPythonPackage = legacy_pkgs.python39.pkgs.buildPythonPackage;
    fetchPypi = legacy_pkgs.python3Packages.fetchPypi;
  };
  pythonPkgs = import ./build/deps {
    inherit lib legacy_pkgs system local_lib;
    pythonPkgs = legacy_pkgs.python39Packages;
  };
  self_pkgs = import ./build/pkg {
    inherit src lib metadata pythonPkgs;
  };
  checks = import ./check {self_pkg = self_pkgs.pkg;};
in
  self_pkgs // {check = checks;}

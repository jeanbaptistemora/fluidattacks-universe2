{
  legacy_pkgs,
  src,
}: let
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).tool.poetry;
  lib = {
    buildEnv = legacy_pkgs.python39.buildEnv.override;
    buildPythonPackage = legacy_pkgs.python39.pkgs.buildPythonPackage;
    fetchPypi = legacy_pkgs.python3Packages.fetchPypi;
  };
  pythonPkgs = import ./build/deps {
    inherit lib;
    pythonPkgs = legacy_pkgs.python39Packages;
  };
  self_pkgs = import ./build/pkg {
    inherit src lib metadata pythonPkgs;
  };
in
  self_pkgs

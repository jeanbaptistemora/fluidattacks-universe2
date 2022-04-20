{
  legacy_pkgs,
  src,
}: let
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).tool.poetry;
  lib = {
    buildEnv = legacy_pkgs.python38.buildEnv.override;
    buildPythonPackage = legacy_pkgs.python38.pkgs.buildPythonPackage;
    fetchPypi = legacy_pkgs.python3Packages.fetchPypi;
  };
  pythonPkgs = legacy_pkgs.python38Packages;
  self_pkgs = import ./build/pkg {
    inherit src lib metadata pythonPkgs;
  };
  checks = import ./ci/check.nix {self_pkg = self_pkgs.pkg;};
in
  self_pkgs // {check = checks;}

{
  legacy_pkgs,
  python_version,
  src,
}: let
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).tool.poetry;
  lib = {
    buildEnv = legacy_pkgs."${python_version}".buildEnv.override;
    buildPythonPackage = legacy_pkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = legacy_pkgs.python3Packages.fetchPypi;
  };
  python_pkgs = import ./build/deps {
    inherit lib;
    pythonPkgs = legacy_pkgs."${python_version}Packages";
  };
  self_pkgs = import ./build/pkg {
    inherit src lib metadata python_pkgs;
  };
in
  self_pkgs

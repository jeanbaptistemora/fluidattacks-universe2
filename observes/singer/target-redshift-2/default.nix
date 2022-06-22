{
  observesIndex,
  nixpkgs,
  projectPath,
  python_version,
  src,
  system,
}: let
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).tool.poetry;
  lib = {
    buildEnv = nixpkgs."${python_version}".buildEnv.override;
    buildPythonPackage = nixpkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = nixpkgs.python3Packages.fetchPypi;
  };
  python_pkgs = import ./build/deps {
    inherit observesIndex nixpkgs lib projectPath python_version system;
  };
  self_pkgs = import ./build/pkg {
    inherit src lib metadata python_pkgs;
  };
  checks = import ./check {self_pkg = self_pkgs.pkg;};
in
  self_pkgs // {check = checks;}

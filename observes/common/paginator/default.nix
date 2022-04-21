{
  legacyPkgs,
  localLib,
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
  pythonPkgs = import ./build/deps {
    inherit legacyPkgs lib localLib pythonVersion system;
    pythonPkgs = legacyPkgs."${pythonVersion}Packages";
  };
  self_pkgs = import ./build/pkg {
    inherit src lib metadata pythonPkgs;
  };
in
  self_pkgs

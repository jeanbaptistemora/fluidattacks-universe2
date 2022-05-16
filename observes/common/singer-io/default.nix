{
  pkgs,
  local_pkgs,
  python_version,
  src,
}: let
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).tool.poetry;
  lib = {
    buildEnv = pkgs."${python_version}".buildEnv.override;
    buildPythonPackage = pkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = pkgs.python3Packages.fetchPypi;
  };
  pythonPkgs = import ./build/deps {
    inherit pkgs lib local_pkgs python_version;
  };
  self_pkgs = import ./build/pkg {
    inherit src lib metadata pythonPkgs;
  };
in
  self_pkgs

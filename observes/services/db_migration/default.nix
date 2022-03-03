{ system, legacy_pkgs, local_lib, src }:
let
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).tool.poetry;
  lib = {
    buildPythonPackage = legacy_pkgs.python39.pkgs.buildPythonPackage;
    fetchPypi = legacy_pkgs.python3Packages.fetchPypi;
  };
  pythonPkgs = import ./build/deps {
    inherit legacy_pkgs system local_lib;
    pythonPkgs = legacy_pkgs.python39Packages;
  };
  self_pkgs = import ./build/pkg {
    inherit src lib metadata pythonPkgs;
  };
  build_env = pkg: legacy_pkgs.python39.buildEnv.override {
    extraLibs = [ pkg ];
    ignoreCollisions = false;
  };
in
{
  env.runtime = build_env self_pkgs.runtime;
  env.dev = build_env self_pkgs.dev;
  pkg = self_pkgs.runtime;
}

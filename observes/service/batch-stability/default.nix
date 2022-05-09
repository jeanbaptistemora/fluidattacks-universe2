{
  legacy_pkgs,
  extras,
  src,
}: let
  python_version = "python39";
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).tool.poetry;
  lib = {
    buildEnv = legacy_pkgs."${python_version}".buildEnv.override;
    buildPythonPackage = legacy_pkgs."${python_version}".pkgs.buildPythonPackage;
    fetchPypi = legacy_pkgs.python3Packages.fetchPypi;
  };
  python_pkgs =
    import ./build/deps {
      inherit lib;
      python_pkgs = legacy_pkgs."${python_version}Packages";
    }
    // {
      utils-logger = extras.utils-logger."${python_version}".pkg;
    };
  self_pkgs = import ./build/pkg {
    inherit src lib metadata python_pkgs;
  };
  checks = import ./ci/check.nix {self_pkg = self_pkgs.pkg;};
in
  self_pkgs // {check = checks;}

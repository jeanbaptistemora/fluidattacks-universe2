{
  legacyPkgs,
  localLib,
  pythonVersion,
  src,
  system,
}: let
  purity_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    ref = "refs/tags/v1.15.0";
  };
  purity = import purity_src {
    inherit system;
    legacy_pkgs = legacyPkgs;
    src = purity_src;
  };
  singer_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/singer_io";
    ref = "refs/tags/v1.1.0";
  };
  singer = import singer_src {
    inherit system purity legacyPkgs;
    src = singer_src;
  };
  metadata = (builtins.fromTOML (builtins.readFile "${src}/pyproject.toml")).tool.poetry;
  lib = {
    buildEnv = legacyPkgs."${pythonVersion}".buildEnv.override;
    buildPythonPackage = legacyPkgs."${pythonVersion}".pkgs.buildPythonPackage;
    fetchPypi = legacyPkgs.python3Packages.fetchPypi;
  };
  pkgs =
    legacyPkgs
    // {
      "${pythonVersion}Packages" =
        legacyPkgs."${pythonVersion}Packages"
        // {
          fa-purity = purity."${pythonVersion}".pkg;
          fa-singer-io = singer."${pythonVersion}".pkg;
        };
    };
  pythonPkgs = import ./build/deps {
    inherit system lib localLib pythonVersion;
    legacyPkgs = pkgs;
  };
  self_pkgs = import ./build/pkg {
    inherit src lib metadata pythonPkgs;
  };
  checks = import ./check {self_pkg = self_pkgs.pkg;};
in
  self_pkgs // {check = checks;}

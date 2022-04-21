{
  legacyPkgs,
  lib,
  pythonPkgs,
  pythonVersion,
  system,
}: let
  purity_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    ref = "refs/tags/v1.13.0";
  };
  purity = import purity_src {
    inherit system;
    legacy_pkgs = legacyPkgs;
    src = purity_src;
  };
  returns = import ./returns {
    inherit lib pythonPkgs;
  };
in
  pythonPkgs
  // {
    inherit returns;
    fa-purity = purity."${pythonVersion}".pkg;
  }

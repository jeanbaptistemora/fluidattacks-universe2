{
  lib,
  system,
  local_lib,
  legacy_pkgs,
  pythonPkgs,
}: let
  python_version = "python39";
  purity_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    rev = "4515a1af33cfaf249bf32afc7e8f0b7735959679";
    ref = "refs/tags/v1.5.1";
  };
  purity = import purity_src {
    inherit system legacy_pkgs python_version;
    self = purity_src;
    path_filter = {root, ...}: root;
  };
in
  pythonPkgs
  // {
    import-linter = import ./import-linter {
      inherit lib;
      click = pythonPkgs.click;
      networkx = pythonPkgs.networkx;
    };
    purity = purity.pkg;
    types-click = import ./click/stubs.nix lib;
    utils-logger =
      (import local_lib.utils-logger {
        src = local_lib.utils-logger;
        inherit python_version legacy_pkgs;
      })
      .pkg;
  }

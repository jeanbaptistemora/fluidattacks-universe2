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
    returns = import ./returns.nix {inherit lib pythonPkgs;};
    purity = purity.pkg;
    utils-logger =
      (import local_lib.utils-logger {
        src = local_lib.utils-logger;
        inherit python_version legacy_pkgs;
      })
      .pkg;
  }

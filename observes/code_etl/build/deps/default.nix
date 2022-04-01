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
    ref = "refs/tags/v1.8.0";
  };
  purity = import purity_src {
    inherit system legacy_pkgs;
    src = purity_src;
  };
  utils-logger = import local_lib.utils-logger {
    src = local_lib.utils-logger;
    inherit python_version legacy_pkgs;
  };
in
  pythonPkgs
  // {
    import-linter = import ./import-linter {
      inherit lib pythonPkgs;
    };
    fa-purity = purity."${python_version}".pkg;
    types-click = import ./click/stubs.nix lib;
    utils-logger = utils-logger.pkg;
  }

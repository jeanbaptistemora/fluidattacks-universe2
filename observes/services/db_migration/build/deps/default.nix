{
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
  redshift_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/redshift_client";
    ref = "refs/tags/v0.5.2";
  };
  redshift = import redshift_src {
    inherit system legacy_pkgs python_version;
    src = redshift_src;
    others = {
      fa-purity = purity.pkg;
    };
  };
in
  pythonPkgs
  // {
    redshift-client = redshift.pkg;
    utils-logger =
      (import local_lib.utils-logger {
        src = local_lib.utils-logger;
        inherit python_version legacy_pkgs;
      })
      .pkg;
  }

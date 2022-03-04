{ system, local_lib, legacy_pkgs, pythonPkgs }:
let
  python_version = "python39";
  purity_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    ref = "main";
    rev = "bcabbec2b6728f6d24d965849ef63c01143926c2";
  };
  purity = import purity_src {
    inherit system legacy_pkgs python_version;
    self = purity_src;
    path_filter = { root, ... }: root;
  };
  redshift_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/redshift_client";
    ref = "main";
    rev = "cafb83991ac3f23833f0213fd8be615ac1c114ea";
  };
  redshift = import redshift_src {
    inherit system legacy_pkgs python_version;
    self = redshift_src;
    path_filter = { root, ... }: root;
    others = {
      fa-purity = purity.pkg;
    };
  };
in
pythonPkgs // {
  redshift-client = redshift.pkg;
  utils-logger = (import local_lib.utils-logger {
    src = local_lib.utils-logger;
    inherit python_version legacy_pkgs;
  }).pkg;
}

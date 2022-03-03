{ system, legacy_pkgs, pythonPkgs }:
let
  purity_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    ref = "main";
    rev = "bcabbec2b6728f6d24d965849ef63c01143926c2";
  };
  purity = import purity_src {
    inherit system legacy_pkgs;
    self = purity_src;
    python_version = "python39";
    path_filter = { root, ... }: root;
  };
  redshift_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/redshift_client";
    ref = "main";
    rev = "fdbf04aa374490f5006fe9365ed3993dee8d468c";
  };
  redshift = import redshift_src {
    inherit system legacy_pkgs;
    self = redshift_src;
    python_version = "python39";
    path_filter = { root, ... }: root;
    others = {
      fa-purity = purity.pkg;
    };
  };
in
pythonPkgs // {
  redshift-client = redshift.pkg;
}

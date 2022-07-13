{nixpkgs}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    ref = "refs/tags/v1.21.1";
  };
in
  import src {
    inherit src nixpkgs;
  }

{nixpkgs}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    rev = "45ddbd204ab1f75180f165f50188f2e59371c26a";
    ref = "refs/tags/v1.27.0";
  };
in
  import src {
    inherit src nixpkgs;
  }

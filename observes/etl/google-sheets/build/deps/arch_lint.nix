{nixpkgs}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/arch_lint";
    rev = "b2d79d8824dfd1b8f191777c006ab208d38352e3";
    ref = "refs/tags/v2.3.0";
  };
in
  import src {
    inherit src nixpkgs;
  }

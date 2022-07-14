{nixpkgs}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/singer_io";
    ref = "refs/tags/v1.4.0";
  };
in
  import src {
    inherit src nixpkgs;
  }

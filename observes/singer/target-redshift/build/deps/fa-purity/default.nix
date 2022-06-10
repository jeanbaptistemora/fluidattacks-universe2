{
  system,
  nixpkgs,
}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    ref = "refs/tags/v1.18.1";
  };
in
  import src {
    inherit src system;
    legacy_pkgs = nixpkgs;
  }

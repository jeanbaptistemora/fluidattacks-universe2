{
  system,
  purity,
  nixpkgs,
}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/singer_io";
    ref = "refs/tags/v1.1.0";
  };
in
  import src {
    inherit purity src system;
    legacyPkgs = nixpkgs;
  }

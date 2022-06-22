{
  system,
  purity,
  nixpkgs,
}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/redshift_client";
    ref = "refs/tags/v0.7.0";
  };
in
  import src {
    inherit src system;
    legacy_pkgs = nixpkgs;
    others = {
      fa-purity = purity.packages."${system}";
    };
  }

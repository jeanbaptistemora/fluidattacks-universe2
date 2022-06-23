{
  purity,
  nixpkgs,
}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/redshift_client";
    ref = "refs/tags/v0.8.0";
  };
in
  import src {
    inherit src;
    legacy_pkgs = nixpkgs;
    others = {
      fa-purity = purity;
    };
  }

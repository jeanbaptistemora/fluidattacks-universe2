{
  purity,
  nixpkgs,
}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/redshift_client";
    ref = "refs/tags/v0.9.2";
  };
in
  import src {
    inherit src;
    legacy_pkgs = nixpkgs;
    others = {
      fa-purity = purity;
    };
  }

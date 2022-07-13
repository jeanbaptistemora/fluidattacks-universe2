{
  system,
  nixpkgs,
}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/singer_io";
    ref = "main";
    rev = "5a9421e3323e4e8b701fa702b8157139298cf43f";
  };
in
  import src {
    inherit purity src system;
    purity = nixpkgs.purity;
    legacyPkgs = nixpkgs;
  }

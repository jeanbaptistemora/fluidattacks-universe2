{
  system,
  nixpkgs,
}: let
  src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    ref = "main";
    rev = "1816492d1ac416becac6bcdd9ebb9b1be06ffddd";
  };
in
  import src {
    inherit src system;
    legacy_pkgs = nixpkgs;
  }

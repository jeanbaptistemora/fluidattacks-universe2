let
  src = import ./src/fetch-src.nix {
    repo = "https://github.com/NixOS/nixpkgs";
    commit = "5d5e970ce04933576957dfbf99cb7d4c1802c60d";
    digest = "0sz2bk9k60wb75z8q8wjfihm35xnrqs278pxifqns7zi5ai6q3ns";
  };
in
  import src { }

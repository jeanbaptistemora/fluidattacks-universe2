let
  src = import ./serves-src.nix;
in
  import src { }

let
  pkgs = import ../pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation rec {
    name = "builder";

    buildInputs = [];
  }

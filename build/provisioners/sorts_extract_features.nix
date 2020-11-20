let
  pkgs = import ../pkgs/sorts.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.awscli
        pkgs.git
        pkgs.nix
      ];

      product = import ../../default.nix;
    })
  )

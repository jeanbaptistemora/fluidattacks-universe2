let
  pkgs = import ../pkgs/reviews.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.nix
      ];

      srcProduct = import ../..;
    })
  )

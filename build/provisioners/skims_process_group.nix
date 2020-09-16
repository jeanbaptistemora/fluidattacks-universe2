let
  pkgs = import ../pkgs/skims.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.awscli
        pkgs.git
        pkgs.jq
        pkgs.nix
        pkgs.yq
      ];

      product = import ../../default.nix;
    })
  )

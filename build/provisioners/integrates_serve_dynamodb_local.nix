let
  pkgs = import ../pkgs/integrates.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (import ../src/dynamodb-local.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.unzip
        pkgs.openjdk
        pkgs.awscli
        pkgs.jq
      ];
    })
  )

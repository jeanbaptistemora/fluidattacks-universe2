let
  pkgs = import ../pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.awscli
        pkgs.git
        pkgs.glibc
        pkgs.jq
        pkgs.nodejs
        pkgs.openjdk
        pkgs.sops
      ];

      androidSdk = pkgs.androidenv.androidPkgs_9_0.androidsdk;
    })
  )

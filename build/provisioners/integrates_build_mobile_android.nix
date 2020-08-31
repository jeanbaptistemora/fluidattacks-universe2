let
  pkgs = import ../pkgs/integrates.nix;
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

      androidSdk = (pkgs.androidenv.composeAndroidPackages {
        abiVersions = [ "x86" "x86_64" ];
        platformVersions = [ "29" ];
      }).androidsdk;
    })
  )

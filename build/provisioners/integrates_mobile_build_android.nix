let
  pkgs = import ../pkgs/integrates_mobile.nix;
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
        pkgs.nodejs-12_x
        pkgs.openjdk8_headless
        pkgs.sops
      ];

      androidSdk = (pkgs.androidenv.composeAndroidPackages {
        buildToolsVersions = [ "29.0.2" "30.0.3" ];
        platformVersions = [ "29" ];
      }).androidsdk;
    })
  )

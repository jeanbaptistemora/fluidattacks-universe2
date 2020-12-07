let
  pkgs = import ../pkgs/observes.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.awscli
        pkgs.sops
        pkgs.jq
        pkgs.python38Packages.psycopg2
      ];
      StreamerZoho = pkgs.poetry2nix.mkPoetryApplication {
        projectDir = ../../observes/singer/streamer_zoho_crm;
        python = pkgs.python38;
      };
    })
  )

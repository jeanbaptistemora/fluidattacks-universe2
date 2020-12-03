let
  pkgs = import ../pkgs/observes.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (rec {
      name = "streamer_zoho_crm_test";

      buildInputs = [
        pkgs.git
        pkgs.python38
        pkgs.postgresql
        pkgs.python38Packages.setuptools
      ];

      StreamerZoho = pkgs.poetry2nix.mkPoetryEnv {
        projectDir = ../../observes/singer/streamer_zoho_crm;
        python = pkgs.python38;
      };

    })
  )

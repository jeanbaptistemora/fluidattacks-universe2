let
  pkgs = import ../pkgs/observes.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (rec {
      name = "zoho_crm_test";

      buildInputs = [
        pkgs.git
        pkgs.python38
      ];

      TargetRedshift = pkgs.poetry2nix.mkPoetryEnv {
        projectDir = ../../observes/etl/zoho_crm_etl;
        python = pkgs.python38;
      };

    })
  )

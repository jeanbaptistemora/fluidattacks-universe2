let
  pkgs = import ../pkgs/observes.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
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
        TapCsv
        TapJson
      ];
      StreamerZoho = pkgs.poetry2nix.mkPoetryApplication {
        projectDir = ../../observes/singer/streamer_zoho_crm;
        python = pkgs.python38;
      };
      TapCsv = pkgs.poetry2nix.mkPoetryApplication {
        projectDir = ../../observes/singer/tap_csv;
        python = pkgs.python38;
      };
      TapJson = pkgs.poetry2nix.mkPoetryApplication {
        projectDir = ../../observes/singer/tap_json;
        python = pkgs.python38;
      };
      pyPkgTargetRedshift = builders.pythonPackageLocal {
        path = ../../observes/singer/target_redshift;
        python = pkgs.python38;
      };

    })
  )

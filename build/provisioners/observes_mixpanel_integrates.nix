let
  pkgs = import ../pkgs/observes.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (rec {
      name = "mixpanel_integrates_etl";

      buildInputs = [
        pkgs.git
        pkgs.awscli
        pkgs.sops
        pkgs.jq
        SingerIO
        TapMixpanel
        TapJson
      ];

      SingerIO = pkgs.poetry2nix.mkPoetryApplication {
        projectDir = ../../observes/common/singer_io;
        python = pkgs.python38;
      };

      TapMixpanel = pkgs.poetry2nix.mkPoetryApplication {
        projectDir = ../../observes/singer/tap_mixpanel;
      };

      TapJson = pkgs.poetry2nix.mkPoetryApplication {
        projectDir = ../../observes/singer/tap_json;
      };

      pyPkgTargetRedshift = builders.pythonPackageLocal { path = ../../observes/singer/target_redshift; };
    })
  )

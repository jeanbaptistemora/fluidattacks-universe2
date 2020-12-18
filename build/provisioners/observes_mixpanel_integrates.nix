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
        TapMixpanel
        TapJson
      ];    

      TapMixpanel = pkgs.poetry2nix.mkPoetryApplication {
        projectDir = ../../observes/singer/tap_mixpanel;
      };

      TapJson = pkgs.poetry2nix.mkPoetryApplication {
        projectDir = ../../observes/singer/tap_json;
      };
      
      pyPkgTargetRedshift = builders.pythonPackageLocal { path = ../../observes/singer/target_redshift; };
    })
  )

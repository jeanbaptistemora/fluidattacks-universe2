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
      ];
      pyPkgRequests = builders.pythonPackage {
        requirement = "requests==2.22.0";
      };      

      pyPkgTapMixpanel = builders.pythonPackageLocal {
        path = ../../observes/singer/tap_mixpanel;
      };

      pyPkgTapjson = builders.pythonPackageLocal {
        path = ../../observes/singer/tap_json;
      };
      
      pyPkgTargetRedshift = builders.pythonPackageLocal { path = ../../observes/singer/target_redshift; };
    })
  )

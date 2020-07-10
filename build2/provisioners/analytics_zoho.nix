let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
in
  pkgs.stdenv.mkDerivation (
        (import ../src/basic.nix)
    //  (import ../src/external.nix pkgs)
    //  (rec {
          name = "builder";

          buildInputs = [
            pkgs.git
            pkgs.awscli
            pkgs.sops
            pkgs.jq
          ];

          pyPkgRequests = builders.pythonPackage "requests==2.24.0";

          pyPkgTapjson = builders.pythonPackageLocal ../../analytics/singer/tap_json;
          pyPkgTargetRedshift = builders.pythonPackageLocal ../../analytics/singer/target_redshift;
        })
  )

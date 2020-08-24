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

          pyPkgAioextensions = builders.pythonPackage {
            requirement = "aioextensions==20.8.1478538";
          };
          pyPkgAiohttp = builders.pythonPackage {
            requirement = "aiohttp==3.6.2";
          };
          pyPkgTapjson = builders.pythonPackageLocal { path = ../../observes/singer/tap_json; };
          pyPkgTargetRedshift = builders.pythonPackageLocal { path = ../../observes/singer/target_redshift; };
        })
  )

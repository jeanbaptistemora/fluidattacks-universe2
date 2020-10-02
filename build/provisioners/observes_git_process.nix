let
  pkgs = import ../pkgs/observes.nix;
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
            pkgs.python37
          ];

          pyPkgMelts = import ../../melts pkgs;
          pyPkgTapgit = builders.pythonPackageLocal { path = ../../observes/singer/tap_git; };
          pyPkgTracers = builders.pythonPackage { requirement = "tracers==20.7.1645"; };
        })
  )

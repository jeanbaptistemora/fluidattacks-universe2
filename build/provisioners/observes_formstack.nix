let
  pkgs = import ../pkgs/observes.nix;
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

          pyPkgTapformstack = builders.pythonPackageLocal { path = ../../observes/singer/tap_formstack; };
          pyPkgTargetRedshift = builders.pythonPackageLocal { path = ../../observes/singer/target_redshift; };
        })
  )

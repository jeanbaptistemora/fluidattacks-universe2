let
  pkgs = import ../pkgs/stable.nix;
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

          pyPkgTapformstack = builders.pythonPackageLocal ../../analytics/singer/tap_formstack;
          pyPkgTargetRedshift = builders.pythonPackageLocal ../../analytics/singer/target_redshift;
        })
  )

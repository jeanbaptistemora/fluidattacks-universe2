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
          ];

          pyPkgTapjson = builders.pythonPackageLocal { path = ../../observes/singer/tap_json; };
          pyPkgTargetRedshift = builders.pythonPackageLocal { path = ../../observes/singer/target_redshift; };
          pyPkgStreamerGitlab = builders.pythonPackageLocal { path = ../../observes/singer/streamer_gitlab; };
        })
  )

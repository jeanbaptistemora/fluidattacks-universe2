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

          pyPkgStreamerinfrastructure = builders.pythonPackageLocal { path = ../../serves/analytics/singer/streamer_infrastructure; };
          pyPkgTapjson = builders.pythonPackageLocal { path = ../../serves/analytics/singer/tap_json; };
          pyPkgTargetRedshift = builders.pythonPackageLocal { path = ../../serves/analytics/singer/target_redshift; };
        })
  )

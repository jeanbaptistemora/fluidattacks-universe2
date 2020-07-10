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

          pyPkgStreamerintercom = builders.pythonPackageLocal ../../analytics/singer/streamer_mandrill;
          pyPkgTapjson = builders.pythonPackageLocal ../../analytics/singer/tap_json;
          pyPkgTargetRedshift = builders.pythonPackageLocal ../../analytics/singer/target_redshift;
        })
  )

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
            pkgs.python38Packages.psycopg2
          ];
          EtlGitlab = pkgs.poetry2nix.mkPoetryApplication {
            projectDir = ../../observes/etl/dif_gitlab_etl;
            python = pkgs.python38;
          };
          pyPkgTapjson = builders.pythonPackageLocal {
            path = ../../observes/singer/tap_json;
          };
          pyPkgTargetRedshift = builders.pythonPackageLocal {
            path = ../../observes/singer/target_redshift;
            python = pkgs.python38;
          };

        })
  )

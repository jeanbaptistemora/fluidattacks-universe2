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
            pkgs.cacert
            pkgs.sops
            pkgs.jq
            pkgs.nix
            pkgs.openssh
            pkgs.python37
            pkgs.python37Packages.GitPython
            pkgs.python37Packages.psycopg2
            pkgs.python38Packages.psycopg2
          ];

          UpdateSyncStamp = pkgs.poetry2nix.mkPoetryApplication {
            projectDir = ../../observes/services/update_s3_last_sync_date;
            python = pkgs.python38;
          };

          srcProduct = import ../..;
        })
  )

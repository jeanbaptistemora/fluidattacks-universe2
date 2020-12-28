let
  pkgs = import ../pkgs/observes.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (rec {
      name = "postgres_client_test";

      buildInputs = [
        pkgs.git
        pkgs.postgresql
        pkgs.python38
        pkgs.python38Packages.setuptools
      ];

      PostgresClient = pkgs.poetry2nix.mkPoetryEnv {
        projectDir = ../../observes/common/postgres_client;
        python = pkgs.python38;
      };

    })
  )

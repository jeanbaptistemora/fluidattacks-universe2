let
  pkgs = import ../pkgs/observes.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (rec {
      name = "tap_csv_test";

      buildInputs = [
        pkgs.git
        pkgs.python38
      ];

      TapCsv = pkgs.poetry2nix.mkPoetryEnv {
        projectDir = ../../observes/singer/tap_csv;
        python = pkgs.python38;
      };

    })
  )

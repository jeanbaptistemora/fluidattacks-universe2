let
  pkgs = import ../pkgs/observes.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (rec {
      name = "singer_io_test";

      buildInputs = [
        pkgs.git
        pkgs.python38
      ];

      SingerIO = pkgs.poetry2nix.mkPoetryEnv {
        projectDir = ../../observes/common/singer_io;
        python = pkgs.python38;
      };

    })
  )

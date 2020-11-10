let
  pkgs = import ../pkgs/observes.nix;
in
  pkgs.stdenv.mkDerivation (
        (import ../src/basic.nix)
    //  (rec {
          name = "target_redshift_2";

          buildInputs = [
            pkgs.git
            pkgs.python38
          ];

          TargetRedshift = pkgs.poetry2nix.mkPoetryEnv {
            projectDir = ../../observes/singer/target_redshift_2;
            python = pkgs.python38;
          };

        })
  )

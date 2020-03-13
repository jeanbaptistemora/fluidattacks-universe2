let
  pkgs = import ../pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (rec {
      name = "builder";

      buildInputs = []
        ++ [
          pkgs.git
          pkgs.awscli
          pkgs.terraform
          pkgs.tflint
        ];
    })
  )

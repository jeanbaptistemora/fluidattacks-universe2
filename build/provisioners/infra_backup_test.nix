let
  pkgs = import ../pkgs/stable.nix;
  pkgs-unstable = import ../pkgs/unstable.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.awscli
        pkgs-unstable.terraform
        pkgs.tflint
      ];
    })
  )

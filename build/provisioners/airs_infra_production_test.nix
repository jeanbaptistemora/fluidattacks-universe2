let
  pkgs = import ../pkgs/airs.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.glibcLocales
        pkgs.awscli
        pkgs.terraform
        pkgs.tflint
      ];
    })
  )

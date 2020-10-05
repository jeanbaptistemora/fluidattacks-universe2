let
  pkgs = import ../pkgs/serves.nix;
in
  pkgs.stdenv.mkDerivation (
        (import ../src/basic.nix)
    //  (import ../src/external.nix pkgs)
    //  (rec {
          name = "builder";

          buildInputs = [
            pkgs.git
            pkgs.awscli
            pkgs.terraform_0_13
          ];
        })
  )

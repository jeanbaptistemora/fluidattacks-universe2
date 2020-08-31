let
  pkgs = import ../pkgs/observes.nix;
  pkgs-terraform = import ../pkgs/terraform-0-13.nix;
in
  pkgs.stdenv.mkDerivation (
        (import ../src/basic.nix)
    //  (import ../src/external.nix pkgs)
    //  (rec {
          name = "builder";

          buildInputs = [
            pkgs.git
            pkgs.awscli
            pkgs-terraform.terraform_0_13
            pkgs.tflint
          ];
        })
  )

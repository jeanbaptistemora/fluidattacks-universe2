let
  pkgs = import ../pkgs/serves.nix;
  helm-2-pkgs = import ../pkgs/serves-helm-2.nix;
in
  pkgs.stdenv.mkDerivation (
        (import ../src/basic.nix)
    //  (import ../src/external.nix pkgs)
    //  (rec {
          name = "builder";

          buildInputs = [
            pkgs.git
            pkgs.awscli
            pkgs.aws-iam-authenticator
            pkgs.kubectl
            pkgs.sops
            pkgs.jq
            pkgs.terraform_0_13
            pkgs.tflint
            pkgs.envsubst
            helm-2-pkgs.kubernetes-helm
          ];
        })
  )

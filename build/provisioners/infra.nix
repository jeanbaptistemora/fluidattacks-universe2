let
  pkgs = import ../pkgs/stable.nix;
  pkgs-unstable = import ../pkgs/unstable.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = []
        ++ (import ../dependencies/version-control.nix pkgs)
        ++ [
          pkgs.docker
          pkgs.cacert
          pkgs.curl
          pkgs.hostname
          pkgs.jq
          pkgs.rpl
          pkgs.unzip
          pkgs.wget
          pkgs.zip
          pkgs.awscli
          pkgs.sops
          pkgs-unstable.kubectl
          pkgs-unstable.terraform
          pkgs-unstable.tflint
        ];
    })
  )

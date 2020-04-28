let
  pkgs = import ../pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = []
        ++ (import ../dependencies/version-control.nix pkgs)
        ++ [
          pkgs.sysctl
          pkgs.nodejs
          pkgs.awscli
          pkgs.curl
          pkgs.cacert
          pkgs.sops
          pkgs.jq
        ];
    })
  )

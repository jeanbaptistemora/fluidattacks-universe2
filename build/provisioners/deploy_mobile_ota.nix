let
  pkgs = import ../pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.awscli
        pkgs.cacert
        pkgs.curl
        pkgs.git
        pkgs.jq
        pkgs.nodejs
        pkgs.sops
        pkgs.sysctl
      ];
    })
  )

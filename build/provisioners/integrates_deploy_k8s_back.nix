let
  pkgs = import ../pkgs/integrates.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.awscli
        pkgs.kubectl
        pkgs.rpl
        pkgs.sops
        pkgs.jq
        pkgs.curl
        pkgs.cacert
      ];
    })
  )

let
  pkgs = import ../pkgs/common.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.awscli
        pkgs.cacert
        pkgs.git
        pkgs.jq
        pkgs.python37
        pkgs.sops
      ];
    })
  )

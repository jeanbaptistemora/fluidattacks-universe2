let
  pkgs = import ../pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.docker
        pkgs.awscli
        pkgs.sops
        pkgs.jq
        (pkgs.python37.withPackages (ps: with ps; [
          setuptools
        ]))
      ];
    })
  )

let
  pkgs = import ../pkgs/observes.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
in
  pkgs.stdenv.mkDerivation (
        (import ../src/basic.nix)
    //  (import ../src/external.nix pkgs)
    //  (rec {
          name = "builder";

          buildInputs = [
            pkgs.git
            pkgs.awscli
            pkgs.sops
            pkgs.jq
            pkgs.openssh
            pkgs.cacert
            pkgs.nix
            pkgs.python37
          ];

          srcProduct = import ../..;
        })
  )

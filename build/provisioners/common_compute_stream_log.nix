let
  pkgs = import ../pkgs/common.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
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
        pkgs.python37
        pkgs.sops
      ];

      pyPkgAwslogs = builders.pythonPackage {
        requirement = "awslogs==0.14.0";
      };
    })
  )

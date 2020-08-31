let
  pkgs = import ../pkgs/asserts.nix;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.awscli
        pkgs.sops
        pkgs.jq
        pkgs.cacert
      ];

      pyPkgTestrequirements = builders.pythonRequirements ../../asserts/deploy/dependencies/tests.lst;
      pyPkgAsserts = import ../../asserts pkgs;
    })
  )

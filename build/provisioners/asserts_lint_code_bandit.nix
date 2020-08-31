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
        pkgs.python38
      ];

      pyPkgAssertslintrequirements = builders.pythonRequirements ../../asserts/deploy/dependencies/lint_asserts.lst;
    })
  )

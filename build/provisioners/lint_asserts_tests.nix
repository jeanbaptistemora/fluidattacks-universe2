let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.cacert
        pkgs.python37
        pkgs.pre-commit
      ];

      pyPkgAssertslintrequirements = builders.pythonRequirements ../dependencies/lint_asserts.lst;
      pyPkgAsserts = import ../.. pkgs;
    })
  )

let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = [
        pkgs.git
        pkgs.cacert
        pkgs.python37
        pkgs.pre-commit
      ];

      pyPkgAssertstestsrequirements = builders.pythonRequirements ../../asserts/deploy/dependencies/tests.lst;
      pyPkgAssertslintrequirements = builders.pythonRequirements ../../asserts/deploy/dependencies/lint_asserts.lst;
      pyPkgAsserts = import ../../asserts pkgs;
    })
  )

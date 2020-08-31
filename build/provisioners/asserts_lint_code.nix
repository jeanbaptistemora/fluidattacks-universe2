let
  pkgs = import ../pkgs/asserts.nix;
  builders.pythonPackage = import ../builders/python-package pkgs;
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
      ];

      pyPkgAssertstestsrequirements = builders.pythonRequirements ../../asserts/deploy/dependencies/tests.lst;
      pyPkgAssertslintrequirements = builders.pythonRequirements ../../asserts/deploy/dependencies/lint_asserts.lst;
      pyPkgPrecommit = builders.pythonPackage {
        requirement = "pre-commit==2.7.1";
      };
      pyPkgAsserts = import ../../asserts pkgs;
    })
  )

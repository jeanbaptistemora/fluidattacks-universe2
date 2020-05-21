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
      ];

      pyPkgAssertslintrequirements = builders.pythonRequirements ../dependencies/lint_asserts.lst;
    })
  )

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
        pkgs.gnupg
        pkgs.cacert
        pkgs.python37Packages.selenium
        pkgs.python37Packages.brotli
      ];

      pyPkgTestrequirements = builders.pythonRequirements ../dependencies/tests.lst;
      pyPkgAsserts = import ../.. pkgs;
    })
  )

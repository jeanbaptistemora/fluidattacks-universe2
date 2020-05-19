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
        pkgs.unixODBC
        pkgs.python37Packages.selenium
      ];

      pyPkgTestrequirements = builders.pythonRequirements ../dependencies/tests.lst;
      pyPkgAsserts = import ../.. pkgs;
    })
  )

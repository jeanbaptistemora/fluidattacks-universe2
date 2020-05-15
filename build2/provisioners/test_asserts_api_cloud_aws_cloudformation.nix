let
  pkgs = import ../pkgs/stable.nix;
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
  builders.pythonPackageLocal = import ../builders/python-package-local pkgs;
  odbcIniContents = with pkgs.unixODBCDrivers; ''
    [${msodbcsql17.fancyName}]
    Driver=${msodbcsql17}/${msodbcsql17.driver}
  '';
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (rec {
      name = "builder";

      inherit odbcIniContents;

      buildInputs = [
        pkgs.git
        pkgs.postgresql
        pkgs.gnupg
        pkgs.unixODBC
        pkgs.cacert
      ];

      pyPkgTestrequirements = builders.pythonRequirements ../dependencies/tests.lst;
      pyPkgAsserts = builders.pythonPackageLocal ../..;
    })
  )

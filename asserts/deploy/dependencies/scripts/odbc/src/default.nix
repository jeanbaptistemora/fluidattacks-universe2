let
  pkgs = import ../../../../../../build/pkgs/asserts.nix;

  odbcIniContents = with pkgs.unixODBCDrivers; ''
    [${msodbcsql17.fancyName}]
    Driver=${msodbcsql17}/${msodbcsql17.driver}
  '';
in
  pkgs.stdenv.mkDerivation {
    name = "shell";

    genericShellOptions = ../../../../../../build/include/generic/shell-options.sh;
    genericDirs = ../../../../../../build/include/generic/dir-structure.sh;

    inherit odbcIniContents;
    buildInputs = with pkgs; [
      unixODBC
      unixODBCDrivers.msodbcsql17
    ];
  }

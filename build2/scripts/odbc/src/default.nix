let
  pkgs = import ../../../pkgs/stable.nix;

  odbcIniContents = with pkgs.unixODBCDrivers; ''
    [${msodbcsql17.fancyName}]
    Driver=${msodbcsql17}/${msodbcsql17.driver}
  '';
in
  pkgs.stdenv.mkDerivation {
    name = "shell";

    genericShellOptions = ../../../include/generic/shell-options.sh;
    genericDirs = ../../../include/generic/dir-structure.sh;

    inherit odbcIniContents;
    buildInputs = with pkgs; [
      unixODBC
      unixODBCDrivers.msodbcsql17
    ];
  }

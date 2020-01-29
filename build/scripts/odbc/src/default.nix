let
  pkgs = import ../../../pkgs.nix { };
  main = import ../../../main.nix;

  odbcIniContents = with pkgs.unixODBCDrivers; ''
    [${msodbcsql17.fancyName}]
    Driver=${msodbcsql17}/${msodbcsql17.driver}
  '';

in

with main;

pkgs.stdenv.mkDerivation {
  name = "shell";
  inherit genericDirs genericShellOptions;
  inherit odbcIniContents;
  buildInputs = with pkgs; [
    unixODBC
    unixODBCDrivers.msodbcsql17
  ];
}

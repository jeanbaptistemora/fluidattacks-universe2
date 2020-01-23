let
  pkgs = import ./pkgs.nix;
  main = import ./main.nix;
in

with main;

pkgs.stdenv.mkDerivation rec {
  name = "shell";
  inherit genericDirs genericShellOptions;
  buildInputs = basicPythonEnv;
}

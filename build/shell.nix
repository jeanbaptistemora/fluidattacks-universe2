let
  pkgs = import ./pkgs/stable.nix;
in
  pkgs.stdenv.mkDerivation rec {
    name = "builder";

    srcIncludeHelpers = ./include/helpers.sh;
    srcCiScriptsHelpersOthers = ../ci-scripts/helpers/others.sh;
    srcIncludeCli = ./include/cli.sh;
    srcIncludeGenericShellOptions = ./include/generic/shell-options.sh;
    srcIncludeGenericDirStructure = ./include/generic/dir-structure.sh;
  }

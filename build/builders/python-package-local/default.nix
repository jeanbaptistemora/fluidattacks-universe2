pkgs:

let
  customPkgs.python = import ../../pkgs/python pkgs;
in
  path:
    pkgs.stdenv.mkDerivation rec {
      name = "python-package-local";
      inherit path;

      srcIncludeGenericShellOptions = ../../../include/generic/shell-options.sh;
      srcIncludeGenericDirStructure = ../../../include/generic/dir-structure.sh;

      builder = ./builder.sh;
      buildInputs = [
        customPkgs.python
      ];
    }

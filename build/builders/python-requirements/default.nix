pkgs:

let
  customPkgs.python = import ../../pkgs/python pkgs;
in
  path:
    pkgs.stdenv.mkDerivation rec {
      name = "python-requirements";
      inherit path;

      srcIncludeGenericShellOptions = ../../include/generic/shell-options.sh;
      srcIncludeGenericDirStructure = ../../include/generic/dir-structure.sh;

      builder = ./builder.sh;
      propagatedBuildInputs = [
        customPkgs.python
        pkgs.libmysqlclient
        pkgs.postgresql
      ];
    }

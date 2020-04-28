pkgs:

path:
  pkgs.stdenv.mkDerivation rec {
    name = "python-requirements";
    inherit path;

    srcIncludeGenericShellOptions = ../../include/generic/shell-options.sh;
    srcIncludeGenericDirStructure = ../../include/generic/dir-structure.sh;

    builder = ./builder.sh;
    propagatedBuildInputs = [
      (pkgs.python37.withPackages (ps: with ps; [
        matplotlib
        pip
        python_magic
        selenium
        setuptools
        wheel
      ]))
      pkgs.libmysqlclient
      pkgs.postgresql
    ];
  }

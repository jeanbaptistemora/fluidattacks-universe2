pkgs:

path:
  pkgs.stdenv.mkDerivation rec {
    name = "python-requirements";
    inherit path;

    srcIncludeGenericShellOptions = ../../include/generic/shell-options.sh;
    srcIncludeGenericDirStructure = ../../include/generic/dir-structure.sh;

    builder = ./builder.sh;
    buildInputs = [
      (pkgs.python37.withPackages (ps: with ps; [
        wheel
        setuptools
        pip
      ]))
      pkgs.postgresql
      pkgs.unixODBC
    ];
  }

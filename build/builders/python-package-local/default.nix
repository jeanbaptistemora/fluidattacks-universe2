pkgs:

let
  stringToDerivationName = import ../../lambdas/string-to-derivation-name pkgs;
in
  path:
    pkgs.stdenv.mkDerivation rec {
      name = stringToDerivationName (builtins.baseNameOf path);
      inherit path;

      srcIncludeGenericShellOptions = ../../include/generic/shell-options.sh;
      srcIncludeGenericDirStructure = ../../include/generic/dir-structure.sh;

      builder = ./builder.sh;
      buildInputs = [
        (pkgs.python37.withPackages (ps: with ps; [
            matplotlib
            pip
            python_magic
            selenium
            setuptools
            wheel
        ]))
      ];
    }

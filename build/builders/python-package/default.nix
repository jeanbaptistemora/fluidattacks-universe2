pkgs:

let
  stringToDerivationName = import ../../lambdas/string-to-derivation-name pkgs;
in
  { requirement ? "",
    dependencies ? [],
  }:
    pkgs.stdenv.mkDerivation rec {
      name = stringToDerivationName requirement;
      inherit requirement;

      srcIncludeGenericShellOptions = ../../include/generic/shell-options.sh;
      srcIncludeGenericDirStructure = ../../include/generic/dir-structure.sh;

      builder = ./builder.sh;
      propagatedBuildInputs = [
        dependencies
        (pkgs.python37.withPackages (ps: with ps; [
          wheel
          setuptools
          pip
        ]))
      ];
    }

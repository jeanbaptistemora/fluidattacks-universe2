pkgs:

let
  stringToDerivationName = import ../../lambdas/string-to-derivation-name pkgs;
in
  { requirement ? "",
    dependencies ? [],
    python ? pkgs.python37,
    cacheKey ? "",
  }:
    pkgs.stdenv.mkDerivation rec {
      name = stringToDerivationName requirement;
      inherit cacheKey requirement;

      srcIncludeGenericShellOptions = ../../include/generic/shell-options.sh;
      srcIncludeGenericDirStructure = ../../include/generic/dir-structure.sh;

      builder = ./builder.sh;
      propagatedBuildInputs = [
        dependencies
        (python.withPackages (ps: with ps; [
          wheel
          setuptools
          pip
        ]))
      ];
    }

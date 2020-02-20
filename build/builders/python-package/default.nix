pkgs:

let
  customPkgs.python = import ../../pkgs/python pkgs;
  stringToDerivationName = import ../../lambdas/string-to-derivation-name pkgs;
in
  requirement:
    pkgs.stdenv.mkDerivation rec {
      name = stringToDerivationName requirement;
      inherit requirement;

      srcIncludeGenericShellOptions = ../../include/generic/shell-options.sh;
      srcIncludeGenericDirStructure = ../../include/generic/dir-structure.sh;

      builder = ./builder.sh;
      buildInputs = [
        customPkgs.python
      ];
    }

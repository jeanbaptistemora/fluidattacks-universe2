pkgs:

let
  envPython = import ../env/python pkgs;
  stringToDerivationName = import ../string-to-derivation-name pkgs;
in
  requirement:
    pkgs.stdenv.mkDerivation rec {
      name = stringToDerivationName requirement;
      inherit requirement;

      srcIncludeGenericShellOptions = ../../include/generic/shell-options.sh;
      srcIncludeGenericDirStructure = ../../include/generic/dir-structure.sh;

      builder = ./builder.sh;
      buildInputs = [
        envPython
      ];
    }

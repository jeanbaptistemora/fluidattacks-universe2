pkgs:

let
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
          (pkgs.python38.withPackages (ps: with ps; [
            wheel
            setuptools
            pip
          ]))
        ];
      }

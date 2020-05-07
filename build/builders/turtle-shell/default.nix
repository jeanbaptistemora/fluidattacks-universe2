pkgs:

let
  stringToDerivationName = import ../../lambdas/string-to-derivation-name pkgs;
in
  sdkVersion:
    pkgs.stdenv.mkDerivation rec {
      name = stringToDerivationName sdkVersion;
      inherit sdkVersion;

      srcIncludeGenericShellOptions = ../../include/generic/shell-options.sh;
      srcIncludeGenericDirStructure = ../../include/generic/dir-structure.sh;

      builder = ./builder.sh;
      buildInputs = [
        pkgs.nodejs
        pkgs.openjdk
        pkgs.python37
      ];
    }

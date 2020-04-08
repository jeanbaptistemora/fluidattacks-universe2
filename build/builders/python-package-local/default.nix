pkgs:

let
  customPkgs.python = import ../../dependencies/python-with-tools.nix pkgs;
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
        customPkgs.python
      ];
    }

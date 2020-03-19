pkgs:

let
  stringToDerivationName = import ../../lambdas/string-to-derivation-name pkgs;
in
  requirement:
    pkgs.stdenv.mkDerivation (
      (import ../../src/basic.nix)
      // (rec {
        name = stringToDerivationName requirement;
        inherit requirement;

        builder = ./builder.sh;
        buildInputs = [
          (pkgs.python38.withPackages (ps: with ps; [
            wheel
            setuptools
            pip
          ]))
        ];
      })
    )

{ pkgs, inputs }:

let
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
  base = [
    pkgs.git
    pkgs.gnupg
    pkgs.cacert
  ];
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (rec {
      name = "builder";

      buildInputs = base ++ inputs;

      pyPkgTestrequirements = builders.pythonRequirements ../dependencies/tests.lst;
      pyPkgAsserts = import ../.. pkgs;
    })
  )

{ pkgs, inputs }:

let
  builders.pythonRequirements = import ../../../build/builders/python-requirements pkgs;
  base = [
    pkgs.git
    pkgs.awscli
    pkgs.sops
    pkgs.jq
    pkgs.cacert
  ];
in
  pkgs.stdenv.mkDerivation (
       (import ../../../build/src/basic.nix)
    // (import ../../../build/src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = base ++ inputs;

      pyPkgTestrequirements = builders.pythonRequirements ./tests.lst;
      pyPkgAsserts = import ../.. pkgs;
    })
  )

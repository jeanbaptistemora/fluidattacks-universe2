{ pkgs, inputs }:

let
  builders.pythonRequirements = import ../builders/python-requirements pkgs;
  base = [
    pkgs.git
    pkgs.awscli
    pkgs.sops
    pkgs.jq
    pkgs.cacert
  ];
in
  pkgs.stdenv.mkDerivation (
       (import ../src/basic.nix)
    // (import ../src/external.nix pkgs)
    // (rec {
      name = "builder";

      buildInputs = base ++ inputs;

      pyPkgTestrequirements = builders.pythonRequirements ../dependencies/tests.lst;
      pyPkgAsserts = import ../.. pkgs;
    })
  )

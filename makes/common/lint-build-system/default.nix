_ @ {
  commonPkgs,
  ...
}:

let
  makeDerivation = import ../../../makes/utils/make-derivation commonPkgs;
in
  makeDerivation {
    builder = ../../../makes/common/lint-build-system/builder.sh;
    buildInputs = [
      commonPkgs.shellcheck
      commonPkgs.nix-linter
    ];
    envSrcMakes = ../../../makes;
    name = "common-lint-build-system";
  }

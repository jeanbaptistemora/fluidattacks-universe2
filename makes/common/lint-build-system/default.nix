_ @ {
  commonPkgs,
  commonPkgsNixLinter,
  ...
}:

let
  makeDerivation = import ../../../makes/utils/make-derivation commonPkgs;
in
  makeDerivation {
    builder = ../../../makes/common/lint-build-system/builder.sh;
    buildInputs = [
      commonPkgs.shellcheck
      commonPkgsNixLinter.nix-linter
    ];
    envSrcMakes = ../../../makes;
    name = "common-lint-build-system";
  }

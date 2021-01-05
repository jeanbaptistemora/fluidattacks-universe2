_ @ {
  skimsPkgs,
  ...
}:

let
  makeDerivation = import ../../../../makes/utils/make-derivation skimsPkgs;
in
  makeDerivation {
    builder = ./builder.sh;
    buildInputs = [
      skimsPkgs.nodejs
    ];
    envSrc = ../../../../skims/static/parsers/babel;
    name = "skims-parsers-babel";
  }

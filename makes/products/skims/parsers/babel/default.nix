{ path
, skimsPkgs
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path skimsPkgs;
in
makeDerivation {
  builder = path "/makes/products/skims/parsers/babel/builder.sh";
  buildInputs = [
    skimsPkgs.nodejs
  ];
  envSrc = path "/skims/static/parsers/babel";
  name = "skims-parsers-babel";
}

{ path
, skimsPkgs
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") skimsPkgs;
in
makeDerivation {
  builder = ./builder.sh;
  buildInputs = [
    skimsPkgs.nodejs
  ];
  envSrc = (path "/skims/static/parsers/babel");
  name = "skims-parsers-babel";
}

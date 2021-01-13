{ integratesPkgs
, ...
} @ _:
let
  makeDerivation = import ../../../../makes/utils/make-derivation integratesPkgs;
in
makeDerivation {
  builder = ./builder.sh;
  envSrcIntegratesFront = ../../../../integrates/front;
  name = "integrates-lint-front";
}

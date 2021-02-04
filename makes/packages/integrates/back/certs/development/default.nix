{ integratesPkgs
, path
, ...
} @ _:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path integratesPkgs;
in
makeDerivation {
  builder = path "/makes/packages/integrates/back/certs/development/builder.sh";
  buildInputs = [ integratesPkgs.openssl ];
  name = "integrates-back-certs-development";
}

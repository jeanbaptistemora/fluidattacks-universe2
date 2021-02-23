{ integratesPkgs
, path
, ...
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path integratesPkgs;
in
makeDerivation {
  builder = path "/makes/packages/integrates/back/certs/development/builder.sh";
  name = "integrates-back-certs-development";
  searchPaths = {
    envPaths = [ integratesPkgs.openssl ];
  };
}

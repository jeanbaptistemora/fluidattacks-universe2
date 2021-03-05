{ nixpkgs2
, path
, ...
}:
let
  makeDerivation = import (path "/makes/utils/make-derivation") path nixpkgs2;
in
makeDerivation {
  builder = path "/makes/packages/integrates/back/certs/development/builder.sh";
  name = "integrates-back-certs-development";
  searchPaths = {
    envPaths = [ nixpkgs2.openssl ];
  };
}

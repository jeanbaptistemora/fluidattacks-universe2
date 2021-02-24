{ observesPkgs
, path
, ...
}:
let
  test = import (path "/makes/libs/observes/test-jobs") {
    inherit path;
    nixPkgs = observesPkgs;
  };
in
test.codeEtlDev

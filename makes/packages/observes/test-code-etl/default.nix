{ observesPkgs
, path
, ...
} @ _:
let
  nixPkgs = observesPkgs;
  test = import (path "/makes/libs/observes/test-jobs") {
    inherit nixPkgs path;
  };
in
test.codeEtlDev

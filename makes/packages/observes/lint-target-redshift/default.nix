{ observesPkgs
, path
, ...
} @ _:
let
  lint = import (path "/makes/libs/observes/lint-jobs") {
    inherit path;
    nixPkgs = observesPkgs;
  };
in
lint.targetRedshift

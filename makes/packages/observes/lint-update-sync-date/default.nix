{ observesPkgs
, path
, ...
} @ _:
let
  nixPkgs = observesPkgs;
  lint = import (path "/makes/libs/observes/lint-jobs") {
    inherit nixPkgs path;
  };
in
lint.updateSyncDate

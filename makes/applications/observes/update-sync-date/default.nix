{ observesPkgs
, path
, ...
}:
let
  nixPkgs = observesPkgs;
  bins = import (path "/makes/libs/observes/bins") {
    inherit path nixPkgs;
  };
in
bins.updateSyncDate

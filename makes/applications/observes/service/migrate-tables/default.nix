{ observesPkgs
, path
, ...
}:
let
  bins = import (path "/makes/libs/observes/bins") {
    inherit path;
    nixPkgs = observesPkgs;
  };
in
bins.serviceMigrateTables

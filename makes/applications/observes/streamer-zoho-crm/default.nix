{ observesPkgs
, path
, ...
} @ _:
let
  nixPkgs = observesPkgs;
  bins = import (path "/makes/libs/observes/bins") {
    inherit nixPkgs path;
  };
in
bins.streamerZohoCrm

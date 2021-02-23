{ observesPkgs
, path
, ...
}:
let
  nixPkgs = observesPkgs;
  bins = import (path "/makes/libs/observes/bins") {
    inherit nixPkgs path;
  };
in
bins.streamerDynamoDB

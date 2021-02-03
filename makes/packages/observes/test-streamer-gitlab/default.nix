{ observesPkgs
, path
, ...
} @ _:
let
  nixPkgs = observesPkgs;
  test = import (path "/makes/libs/observes/test-jobs") {
    inherit path nixPkgs;
  };
in
test.streamerGitlabDev

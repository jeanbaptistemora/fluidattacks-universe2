{ forcesPkgs
, outputs
, path
, ...
} @ _:
let
  makeOci = import (path "/makes/utils/make-oci") path forcesPkgs;
in
makeOci {
  config.WorkingDir = "/src";
  config.Entrypoint = [ outputs.apps."forces/wrapper".program ];
}

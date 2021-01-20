{ outputs
, path
, forcesPkgs
, ...
} @ _:
let
  makeOci = import (path "/makes/utils/make-oci") forcesPkgs;
in
makeOci {
  config.Entrypoint = [ outputs.apps.forces.program ];
}

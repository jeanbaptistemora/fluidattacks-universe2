{ outputs
, path
, skimsPkgs
, ...
} @ _:
let
  makeOci = import (path "/makes/utils/make-oci") skimsPkgs;
in
makeOci {
  config.Entrypoint = [ outputs.apps.skims.program ];
}

{ applications
, path
, skimsPkgs
, ...
} @ _:
let
  makeOci = import (path "/makes/utils/make-oci") path skimsPkgs;
in
makeOci {
  config.Entrypoint = [ applications.skims ];
}

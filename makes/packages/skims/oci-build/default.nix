{ applications
, path
, skimsPkgs
, ...
}:
let
  makeOci = import (path "/makes/utils/make-oci") path skimsPkgs;
in
makeOci {
  config.Entrypoint = [ applications.skims ];
}

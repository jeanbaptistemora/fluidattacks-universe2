{ applications
, path
, nixpkgs
, ...
}:
let
  makeOci = import (path "/makes/utils/make-oci") path nixpkgs;
in
makeOci {
  config.Entrypoint = [ applications.skims ];
}

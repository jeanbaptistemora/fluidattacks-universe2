{ forcesPkgs
, applications
, path
, ...
} @ _:
let
  makeOci = import (path "/makes/utils/make-oci") path forcesPkgs;
in
makeOci {
  config.WorkingDir = "/src";
  config.Entrypoint = [ applications.forces.wrapper ];
}

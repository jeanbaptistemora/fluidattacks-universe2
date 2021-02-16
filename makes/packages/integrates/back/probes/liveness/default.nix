{ integratesPkgs
, packages
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
in
makeEntrypoint {
  arguments = {
    envProbes = packages.integrates.back.probes.lib;
  };
  name = "integrates-back-probes-liveness";
  template = path "/makes/packages/integrates/back/probes/liveness/entrypoint.sh";
}

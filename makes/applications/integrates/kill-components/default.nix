{ integratesPkgs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
in
makeEntrypoint {
  arguments = {
    envKillPidListeningOnPort = import (path "/makes/utils/kill-pid-listening-on-port") path integratesPkgs;
  };
  name = "integrates-kill-components";
  template = path "/makes/applications/integrates/kill-components/entrypoint.sh";
}

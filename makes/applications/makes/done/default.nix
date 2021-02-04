{ makesPkgs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path makesPkgs;
in
makeEntrypoint {
  arguments = {
    envKillPidListeningOnPort = import (path "/makes/utils/kill-pid-listening-on-port") path makesPkgs;
    envNc = "${makesPkgs.netcat}/bin/nc";
  };
  name = "makes-done";
  template = path "/makes/applications/makes/done/entrypoint.sh";
}

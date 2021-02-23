{ makesPkgs
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path makesPkgs;
in
makeEntrypoint {
  arguments = {
    envNc = "${makesPkgs.netcat}/bin/nc";
  };
  name = "makes-wait";
  template = path "/makes/applications/makes/wait/entrypoint.sh";
}

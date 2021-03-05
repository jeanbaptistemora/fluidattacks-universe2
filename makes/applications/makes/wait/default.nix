{ nixpkgs
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envNc = "${nixpkgs.netcat}/bin/nc";
  };
  name = "makes-wait";
  template = path "/makes/applications/makes/wait/entrypoint.sh";
}

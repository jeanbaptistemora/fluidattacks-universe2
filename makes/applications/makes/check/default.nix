{ makesPkgs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path makesPkgs;
in
makeEntrypoint {
  arguments = { };
  name = "makes-check";
  template = path "/makes/applications/makes/check/entrypoint.sh";
}

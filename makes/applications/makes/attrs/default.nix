{ makesPkgs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path makesPkgs;
in
makeEntrypoint {
  arguments = {
    envRoot = path "/";
  };
  name = "makes-attrs";
  template = path "/makes/applications/makes/attrs/template.sh";
}

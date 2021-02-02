{ makesPkgs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path makesPkgs;
in
makeEntrypoint {
  arguments = {
    envFind = "${makesPkgs.findutils}/bin/find";
    envRoot = path "/";
    envSed = "${makesPkgs.gnused}/bin/sed";
  };
  name = "makes-attrs";
  template = path "/makes/applications/makes/attrs/template.sh";
}

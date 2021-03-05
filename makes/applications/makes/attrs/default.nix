{ nixpkgs
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envFind = "${nixpkgs.findutils}/bin/find";
    envRoot = path "/";
    envSed = "${nixpkgs.gnused}/bin/sed";
  };
  name = "makes-attrs";
  template = path "/makes/applications/makes/attrs/template.sh";
}

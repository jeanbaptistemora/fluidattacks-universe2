{ packages
, path
, sortsPkgs
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envPython = "${sortsPkgs.python38}/bin/python";
    envSetupSortsDevelopment = packages.sorts.config-development;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path sortsPkgs;
  };
  name = "sorts-train";
  template = path "/makes/applications/sorts/train/entrypoint.sh";
}

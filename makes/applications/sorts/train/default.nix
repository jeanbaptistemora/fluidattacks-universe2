{ path
, sortsPkgs
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envPython = "${sortsPkgs.python38}/bin/python";
    envSetupSortsDevelopment = import (path "/makes/packages/sorts/config-development") attrs.copy;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path sortsPkgs;
  };
  name = "sorts-train";
  template = path "/makes/applications/sorts/train/entrypoint.sh";
}

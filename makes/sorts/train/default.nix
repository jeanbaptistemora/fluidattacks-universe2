{ path
, sortsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/sorts/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envPython = "${sortsPkgs.python38}/bin/python";
    envSetupSortsDevelopment = config.setupSortsDevelopment;
    envUtilsBashLibAws = import (path "/makes/utils/bash-lib/aws") path sortsPkgs;
  };
  location = "/bin/sorts-train-model-on-aws";
  name = "sorts-train-model-on-aws";
  template = path "/makes/sorts/train/entrypoint.sh";
}

{ sortsPkgs
, ...
} @ attrs:
let
  config = import ../../../makes/sorts/config attrs.copy;
  makeEntrypoint = import ../../../makes/utils/make-entrypoint sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envPython = "${sortsPkgs.python38}/bin/python";
    envSetupSortsDevelopment = config.setupSortsDevelopment;
    envUtilsBashLibAws = import ../../../makes/utils/bash-lib/aws sortsPkgs;
  };
  location = "/bin/sorts-train-model-on-aws";
  name = "sorts-train-model-on-aws";
  template = ../../../makes/sorts/train/entrypoint.sh;
}

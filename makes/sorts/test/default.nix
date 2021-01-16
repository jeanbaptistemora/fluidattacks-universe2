{ sortsPkgs
, ...
} @ attrs:
let
  config = import ../../../makes/sorts/config attrs.copy;
  makeEntrypoint = import ../../../makes/utils/make-entrypoint sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSortsDevelopment = config.setupSortsDevelopment;
    envSetupSortsRuntime = config.setupSortsRuntime;
    envSrcSortsSorts = ../../../sorts/sorts;
  };
  location = "/bin/sorts-test";
  name = "sorts-test";
  template = ../../../makes/sorts/test/entrypoint.sh;
}

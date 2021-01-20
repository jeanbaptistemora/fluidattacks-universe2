{ observesPkgs
, path
, ...
} @ attrs:
let
  config = import (path "/makes/observes/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path observesPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupObservesTargetRedshiftRuntime = config.setupObservesTargetRedshiftRuntime;
  };
  location = "/bin/observes-target-redshift";
  name = "observes-target-redshift-bin";
  template = path "/makes/observes/bin-target-redshift/entrypoint.sh";
}

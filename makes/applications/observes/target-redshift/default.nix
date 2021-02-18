{ observesPkgs
, packages
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path observesPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupObservesTargetRedshiftRuntime = packages.observes.config-target-redshift-runtime;
  };
  name = "observes-target-redshift";
  template = path "/makes/applications/observes/target-redshift/entrypoint.sh";
}

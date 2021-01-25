{ observesPkgs
, path
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path observesPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupObservesTargetRedshiftRuntime = import (path "/makes/packages/observes/config-target-redshift-runtime") attrs.copy;
  };
  name = "observes-target-redshift";
  template = path "/makes/packages/observes/bin-target-redshift/entrypoint.sh";
}

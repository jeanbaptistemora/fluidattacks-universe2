{ nixpkgs2
, packages
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs2;
in
makeEntrypoint {
  arguments = {
    envSetupObservesTargetRedshiftRuntime = packages.observes.config-target-redshift-runtime;
  };
  name = "observes-target-redshift";
  template = path "/makes/applications/observes/target-redshift/entrypoint.sh";
}

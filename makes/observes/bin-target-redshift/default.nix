{ observesPkgs
, ...
} @ attrs:
let
  config = import ../../../makes/observes/config attrs.copy;
  makeEntrypoint = import ../../../makes/utils/make-entrypoint observesPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupObservesTargetRedshiftRuntime = config.setupObservesTargetRedshiftRuntime;
  };
  location = "/bin/observes-target-redshift";
  name = "observes-target-redshift-bin";
  template = ../../../makes/observes/bin-target-redshift/entrypoint.sh;
}

attrs @ {
  outputs,
  skimsBenchmarkOwaspRepo,
  skimsPkgs,
  ...
}:

let
  config = import ../../../makes/skims/config attrs.copy;
  makeEntrypoint = import ../../../makes/utils/make-entrypoint skimsPkgs;
in
  makeEntrypoint {
    arguments = {
      envUtilsBashLibAws = import ../../../makes/utils/bash-lib/aws skimsPkgs;
      envUtilsBashLibSops = import ../../../makes/utils/bash-lib/sops skimsPkgs;
      envBenchmarkRepo = skimsBenchmarkOwaspRepo;
      envPython = "${skimsPkgs.python38}/bin/python";
      envSetupSkimsRuntime = config.setupSkimsRuntime;
      envSkims = outputs.apps.skims.program;
      envSrcSkimsSkims = ../../../skims/skims;
      envSrcSkimsTest = ../../../skims/test;
      envTapJson = outputs.apps.observes-tap-json.program;
      envTargetRedshift = outputs.apps.observes-target-redshift.program;
    };
    location = "/bin/skims-benchmark";
    name = "skims-benchmark";
    template = ../../../makes/skims/benchmark/entrypoint.sh;
  }

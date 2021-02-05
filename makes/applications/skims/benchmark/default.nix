{ applications
, path
, skimsBenchmarkOwaspRepo
, skimsPkgs
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envBenchmarkRepo = skimsBenchmarkOwaspRepo;
    envPython = "${skimsPkgs.python38}/bin/python";
    envSetupSkimsRuntime = import (path "/makes/packages/skims/config-runtime") attrs.copy;
    envSkims = applications.skims;
    envSrcSkimsSkims = path "/skims/skims";
    envSrcSkimsTest = path "/skims/test";
    envTapJson = applications."observes/tap-json";
    envTargetRedshift = applications."observes/target-redshift";
    envUtilsBashLibAws = import (path "/makes/utils/aws") path skimsPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path skimsPkgs;
  };
  name = "skims-benchmark";
  template = path "/makes/applications/skims/benchmark/entrypoint.sh";
}

{ outputs
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
    envSkims = outputs.apps.skims.program;
    envSrcSkimsSkims = path "/skims/skims";
    envSrcSkimsTest = path "/skims/test";
    envTapJson = outputs.apps."observes/tap-json".program;
    envTargetRedshift = outputs.apps."observes/target-redshift".program;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path skimsPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path skimsPkgs;
  };
  name = "skims-benchmark";
  template = path "/makes/applications/skims/benchmark/entrypoint.sh";
}

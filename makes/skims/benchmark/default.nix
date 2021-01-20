{ outputs
, path
, skimsBenchmarkOwaspRepo
, skimsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/skims/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envBenchmarkRepo = skimsBenchmarkOwaspRepo;
    envPython = "${skimsPkgs.python38}/bin/python";
    envSetupSkimsRuntime = config.setupSkimsRuntime;
    envSkims = outputs.apps.skims.program;
    envSrcSkimsSkims = (path "/skims/skims");
    envSrcSkimsTest = (path "/skims/test");
    envTapJson = outputs.apps.observes-tap-json.program;
    envTargetRedshift = outputs.apps.observes-target-redshift.program;
    envUtilsBashLibAws = import (path "/makes/utils/bash-lib/aws") skimsPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/bash-lib/sops") skimsPkgs;
  };
  location = "/bin/skims-benchmark";
  name = "skims-benchmark";
  template = (path "/makes/skims/benchmark/entrypoint.sh");
}

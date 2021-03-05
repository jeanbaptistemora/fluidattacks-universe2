{ applications
, packages
, path
, skimsBenchmarkOwaspRepo
, nixpkgs
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envBenchmarkRepo = skimsBenchmarkOwaspRepo;
    envPython = "${nixpkgs.python38}/bin/python";
    envSetupSkimsRuntime = packages.skims.config-runtime;
    envSkims = applications.skims;
    envSrcSkimsSkims = path "/skims/skims";
    envSrcSkimsTest = path "/skims/test";
    envTapJson = applications.observes.tap-json;
    envTargetRedshift = applications.observes.target-redshift;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixpkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path nixpkgs;
  };
  name = "skims-benchmark";
  template = path "/makes/applications/skims/benchmark/entrypoint.sh";
}

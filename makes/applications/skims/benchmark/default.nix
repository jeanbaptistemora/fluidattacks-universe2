{ makeEntrypoint
, packages
, path
, skimsBenchmarkOwaspRepo
, nixpkgs
, ...
}:
makeEntrypoint {
  arguments = {
    envBenchmarkRepo = skimsBenchmarkOwaspRepo;
    envSrcSkimsSkims = path "/skims/skims";
    envSrcSkimsTest = path "/skims/test";
  };
  name = "skims-benchmark";
  searchPaths = {
    envPaths = [
      nixpkgs.python38
      packages.skims
      packages.observes.tap-json
      packages.observes.target-redshift
    ];
    envSources = [
      packages.skims.config-runtime
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/skims/benchmark/entrypoint.sh";
}

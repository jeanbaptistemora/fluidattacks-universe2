{ packages
, makeEntrypoint
, path
, skimsBenchmarkOwaspRepo
, ...
}:
makeEntrypoint {
  arguments = {
    envBenchmarkRepo = skimsBenchmarkOwaspRepo;
  };
  name = "skims-test";
  searchPaths = {
    envSources = [
      packages.skims.config-development
      packages.skims.config-runtime
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/applications/skims/test/entrypoint.sh";
}

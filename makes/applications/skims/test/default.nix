{ packages
, makeEntrypoint
, path
, skimsBenchmarkOwaspRepo
, skimsVulnerableAppRepo
, ...
}:
makeEntrypoint {
  arguments = {
    envBenchmarkRepo = skimsBenchmarkOwaspRepo;
    envVulnerableAppRepo = skimsVulnerableAppRepo;
  };
  name = "skims-test";
  searchPaths = {
    envPaths = [
      packages.skims.test.mocks.http
    ];
    envSources = [
      packages.skims.config-development
      packages.skims.config-runtime
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/env"
    ];
  };
  template = path "/makes/applications/skims/test/entrypoint.sh";
}

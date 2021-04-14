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
  };
  name = "skims-owasp-benchmark";
  searchPaths = {
    envPaths = [
      nixpkgs.python38
      packages.skims
    ];
    envSources = [
      packages.skims.config-runtime
    ];
  };
  template = path "/makes/applications/skims/owasp-benchmark/entrypoint.sh";
}

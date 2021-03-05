{ buildPythonRequirements
, nixpkgs2
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envGeckoDriver = nixpkgs2.geckodriver;
    envIntegratesEnv = packages.integrates.back.env;
    envFirefox = nixpkgs2.firefox;
  };
  name = "integrates-analytics-snapshots";
  searchPaths = {
    envPaths = [
      nixpkgs2.python37
      packages.integrates.db
      packages.integrates.cache
      packages.integrates.storage
    ];
    envPython37Paths = [
      (buildPythonRequirements {
        name = "integrates-analytics-snapshots";
        requirements = {
          direct = [
            "selenium==3.141.0"
          ];
          inherited = [
            "urllib3==1.26.3"
          ];
        };
        python = nixpkgs2.python37;
      })
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/applications/integrates/analytics/snapshots/entrypoint.sh";
}

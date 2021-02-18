{ buildPythonRequirements
, integratesPkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  arguments = {
    envGeckoDriver = integratesPkgs.geckodriver;
    envIntegratesEnv = packages.integrates.back.env;
    envFirefox = integratesPkgs.firefox;
  };
  name = "integrates-analytics-snapshots";
  searchPaths = {
    envPaths = [
      integratesPkgs.python37
      packages.integrates.db
      packages.integrates.cache
      packages.integrates.storage
    ];
    envPython37Paths = [
      (buildPythonRequirements integratesPkgs {
        name = "integrates-analytics-snapshots";
        requirements = {
          direct = [
            "selenium==3.141.0"
          ];
          inherited = [
            "urllib3==1.26.3"
          ];
        };
        python = integratesPkgs.python37;
      })
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/applications/integrates/analytics/snapshots/entrypoint.sh";
}

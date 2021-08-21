{ makes
, nixpkgs
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envGeckoDriver = nixpkgs.geckodriver;
    envIntegratesEnv = packages.integrates.back.env;
    envFirefox = nixpkgs.firefox;
  };
  name = "integrates-charts-snapshots";
  searchPaths = {
    envPaths = [
      nixpkgs.python37
      packages.integrates.db
      packages.integrates.cache
      packages.integrates.storage
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "integrates-charts-snapshots";
        sourcesYaml = ./sources.yaml;
      })
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/applications/integrates/charts/snapshots/entrypoint.sh";
}

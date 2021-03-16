{ buildPythonRequirements
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
    envPython37Paths = [
      (buildPythonRequirements {
        name = "integrates-charts-snapshots";
        requirements = {
          direct = [
            "selenium==3.141.0"
          ];
          inherited = [
            "urllib3==1.26.3"
          ];
        };
        python = nixpkgs.python37;
      })
    ];
    envUtils = [
      "/makes/utils/aws"
    ];
  };
  template = path "/makes/applications/integrates/charts/snapshots/entrypoint.sh";
}

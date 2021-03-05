{ makeEntrypoint
, observesPkgs
, path
, packages
, ...
}:
makeEntrypoint observesPkgs {
  searchPaths = {
    envPaths = [
      packages.observes.tap-json
      packages.observes.tap-mixpanel
      packages.observes.target-redshift
      packages.observes.update-sync-date
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-mixpanel-integrates-etl";
  template = path "/makes/applications/observes/scheduled/mixpanel-integrates-etl/entrypoint.sh";
}

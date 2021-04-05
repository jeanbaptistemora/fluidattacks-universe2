{ makeEntrypoint
, path
, packages
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.tap-json
      packages.observes.bin.tap-mixpanel
      packages.observes.target-redshift
      packages.observes.bin.service.job-last-success
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-job-mixpanel-integrates-etl";
  template = path "/makes/applications/observes/scheduled/job/mixpanel-integrates-etl/entrypoint.sh";
}

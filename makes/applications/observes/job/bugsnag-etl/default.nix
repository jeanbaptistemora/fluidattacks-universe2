{ makeEntrypoint
, path
, packages
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.tap-bugsnag
      packages.observes.bin.service.job-last-success
      packages.observes.tap-json
      packages.observes.target-redshift
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-job-bugsnag-etl";
  template = path "/makes/applications/observes/job/bugsnag-etl/entrypoint.sh";
}

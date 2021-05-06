{ makeEntrypoint
, path
, packages
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.tap-checkly
      packages.observes.bin.service.job-last-success
      packages.observes.tap-json
      packages.observes.target-redshift
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-job-checkly-etl";
  template = path "/makes/applications/observes/job/checkly-etl/entrypoint.sh";
}

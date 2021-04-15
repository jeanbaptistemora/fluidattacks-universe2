{ makeEntrypoint
, path
, packages
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.tap-delighted
      packages.observes.tap-json
      packages.observes.target-redshift
      packages.observes.bin.service.job-last-success
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-job-delighted-etl";
  template = path "/makes/applications/observes/scheduled/job/delighted-etl/entrypoint.sh";
}

{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.tap-formstack
      packages.observes.target-redshift
      packages.observes.bin.service.job-last-success
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-job-formstack-etl";
  template = path "/makes/applications/observes/scheduled/job/formstack-etl/entrypoint.sh";
}

{ makeEntrypoint
, path
, packages
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.tap-toe-files
      packages.observes.tap-json
      packages.observes.target-redshift
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/git"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-job-toe-files-etl";
  template = path "/makes/applications/observes/scheduled/job/toe-files-etl/entrypoint.sh";
}

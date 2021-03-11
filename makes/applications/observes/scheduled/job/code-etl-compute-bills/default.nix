{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.code-etl
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-job-code-etl-compute-bills";
  template = path "/makes/applications/observes/scheduled/job/code-etl-compute-bills/entrypoint.sh";
}

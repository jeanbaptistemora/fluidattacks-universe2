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
      "/makes/utils/git"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-job-code-etl-amend";
  template = path "/makes/applications/observes/scheduled/job/code-etl-amend/entrypoint.sh";
}

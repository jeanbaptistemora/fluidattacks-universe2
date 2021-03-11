{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.code-etl
      packages.melts
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/git"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-job-code-etl-upload";
  template = path "/makes/applications/observes/scheduled/job/code-etl-upload/entrypoint.sh";
}

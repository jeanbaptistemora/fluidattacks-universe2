{ makeEntrypoint
, path
, packages
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.dif-gitlab-etl
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-job-dif-gitlab-etl";
  template = path "/makes/applications/observes/scheduled/job/dif-gitlab-etl/entrypoint.sh";
}

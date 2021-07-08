{ makeEntrypoint
, path
, packages
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.job.gitlab-etl
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-job-gitlab-etl-default";
  template = path "/makes/applications/observes/job/gitlab-etl/default/entrypoint.sh";
}

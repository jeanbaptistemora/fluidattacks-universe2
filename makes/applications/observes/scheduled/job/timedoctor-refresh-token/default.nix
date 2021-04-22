{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = { };
  searchPaths = {
    envPaths = [
      packages.observes.bin.service.job-last-success
      packages.observes.bin.service.timedoctor-tokens
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/gitlab"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-job-timedoctor-refresh-token";
  template = path "/makes/applications/observes/scheduled/job/timedoctor-refresh-token/entrypoint.sh";
}

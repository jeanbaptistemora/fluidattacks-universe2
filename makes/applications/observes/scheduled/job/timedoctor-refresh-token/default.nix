{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = { };
  searchPaths = {
    envPaths = [
      packages.observes.bin.timedoctor-tokens
      packages.observes.update-sync-date
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

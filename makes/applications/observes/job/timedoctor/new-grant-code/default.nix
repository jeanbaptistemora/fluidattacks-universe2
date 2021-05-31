{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = { };
  searchPaths = {
    envPaths = [
      packages.observes.bin.service.timedoctor-tokens
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-job-timedoctor-new-grant-code";
  template = path "/makes/applications/observes/job/timedoctor/new-grant-code/entrypoint.sh";
}

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
  name = "observes-job-timedoctor-set-init-token";
  template = path "/makes/applications/observes/job/timedoctor/set-init-token/entrypoint.sh";
}

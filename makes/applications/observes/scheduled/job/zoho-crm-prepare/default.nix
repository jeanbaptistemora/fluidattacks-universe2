{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.streamer-zoho-crm
      packages.observes.bin.service.job-last-success
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-job-zoho-crm-prepare";
  template = path "/makes/applications/observes/scheduled/job/zoho-crm-prepare/entrypoint.sh";
}

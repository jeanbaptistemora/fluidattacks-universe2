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
  };
  name = "observes-job-zoho-crm-prepare";
  template = path "/makes/applications/observes/job/zoho-crm-prepare/entrypoint.sh";
}

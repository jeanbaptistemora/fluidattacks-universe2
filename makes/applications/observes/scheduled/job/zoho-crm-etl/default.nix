{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.streamer-zoho-crm
      packages.observes.bin.tap-csv
      packages.observes.tap-json
      packages.observes.target-redshift
      packages.observes.update-sync-date
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-job-zoho-crm-etl";
  template = path "/makes/applications/observes/scheduled/job/zoho-crm-etl/entrypoint.sh";
}

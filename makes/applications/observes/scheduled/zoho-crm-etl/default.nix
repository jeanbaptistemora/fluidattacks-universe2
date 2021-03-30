{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.streamer-zoho-crm
      packages.observes.tap-csv
      packages.observes.tap-json
      packages.observes.target-redshift
      packages.observes.update-sync-date
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-zoho-crm-etl";
  template = path "/makes/applications/observes/scheduled/zoho-crm-etl/entrypoint.sh";
}

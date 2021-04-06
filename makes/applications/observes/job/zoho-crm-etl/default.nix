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
      packages.observes.bin.service.job-last-success
    ];
  };
  name = "observes-job-zoho-crm-etl";
  template = path "/makes/applications/observes/job/zoho-crm-etl/entrypoint.sh";
}

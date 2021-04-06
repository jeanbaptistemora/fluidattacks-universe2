{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.job.zoho-crm-etl
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-job-zoho-crm-etl-fluid";
  template = path "/makes/applications/observes/scheduled/job/zoho-crm-etl/fluid/entrypoint.sh";
}

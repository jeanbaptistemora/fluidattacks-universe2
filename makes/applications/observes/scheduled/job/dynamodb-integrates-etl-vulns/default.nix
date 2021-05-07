{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = { };
  searchPaths = {
    envPaths = [
      packages.observes.job.dynamodb-table-etl
    ];
  };
  name = "observes-scheduled-job-dynamodb-integrates-etl-vulns";
  template = path "/makes/applications/observes/scheduled/job/dynamodb-integrates-etl-vulns/entrypoint.sh";
}

{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = { };
  searchPaths = {
    envPaths = [
      packages.observes.job.dynamodb-etl
    ];
  };
  name = "observes-job-dynamodb-forces-etl";
  template = path "/makes/applications/observes/job/dynamodb-forces-etl/entrypoint.sh";
}

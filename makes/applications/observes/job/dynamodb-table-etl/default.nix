{ makeEntrypoint
, observesPkgs
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = { };
  searchPaths = {
    envPaths = [
      packages.observes.job.dynamodb-etl
      observesPkgs.coreutils
      observesPkgs.jq
    ];
  };
  name = "observes-job-dynamodb-table-etl";
  template = path "/makes/applications/observes/job/dynamodb-table-etl/entrypoint.sh";
}

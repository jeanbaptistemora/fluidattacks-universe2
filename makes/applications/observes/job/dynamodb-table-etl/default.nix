{ makeEntrypoint
, nixpkgs2
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = { };
  searchPaths = {
    envPaths = [
      packages.observes.job.dynamodb-etl
      nixpkgs2.coreutils
      nixpkgs2.jq
    ];
  };
  name = "observes-job-dynamodb-table-etl";
  template = path "/makes/applications/observes/job/dynamodb-table-etl/entrypoint.sh";
}

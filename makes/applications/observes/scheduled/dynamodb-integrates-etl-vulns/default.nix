{ makeEntrypoint
, observesPkgs
, packages
, path
, ...
}:
makeEntrypoint observesPkgs {
  arguments = { };
  searchPaths = {
    envPaths = [
      packages.observes.job.dynamodb-table-etl
    ];
  };
  name = "observes-scheduled-dynamodb-integrates-etl-vulns";
  template = path "/makes/applications/observes/scheduled/dynamodb-integrates-etl-vulns/entrypoint.sh";
}

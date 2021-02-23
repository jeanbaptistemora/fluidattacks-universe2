{ makeEntrypoint
, observesPkgs
, packages
, path
, ...
}:
let
  nixPkgs = observesPkgs;
in
makeEntrypoint nixPkgs {
  arguments = { };
  searchPaths = {
    envPaths = [
      packages.observes.job.dynamodb-etl
      nixPkgs.coreutils
      nixPkgs.jq
    ];
  };
  name = "observes-job-dynamodb-table-etl";
  template = path "/makes/applications/observes/job/dynamodb-table-etl/entrypoint.sh";
}

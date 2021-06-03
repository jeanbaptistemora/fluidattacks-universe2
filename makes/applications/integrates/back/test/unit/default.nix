{ applications
, makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envIntegratesEnv = packages.integrates.back.env;
    envBatchBin = applications.integrates.batch;
  };
  name = "integrates-back-test-unit";
  searchPaths = {
    envSources = [
      packages.integrates.back.pypi.unit-tests
    ];
  };
  template = path "/makes/applications/integrates/back/test/unit/entrypoint.sh";
}

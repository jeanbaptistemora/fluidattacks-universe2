{ makeScript
, outputs
, ...
}:
makeScript {
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-back-test-unit";
  searchPaths = {
    bin = [
      outputs."/integrates/batch"
      outputs."/integrates/cache"
      outputs."/integrates/db"
      outputs."/integrates/storage"
    ];
    source = [
      outputs."/integrates/back/pypi/unit-tests"
    ];
  };
  entrypoint = ./entrypoint.sh;
}

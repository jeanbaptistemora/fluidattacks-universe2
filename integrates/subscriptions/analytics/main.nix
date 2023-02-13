{
  makeScript,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-subscriptions-analytics";
  searchPaths = {
    bin = [
      outputs."/integrates/db"
    ];
    source = [
      outputs."/integrates/storage/dev/lib/populate"
    ];
  };
  entrypoint = ./entrypoint.sh;
}

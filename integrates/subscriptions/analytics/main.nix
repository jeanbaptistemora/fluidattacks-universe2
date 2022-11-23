{
  inputs,
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
      inputs.nixpkgs.python39
      outputs."/integrates/db"
      outputs."/integrates/storage"
    ];
  };
  entrypoint = ./entrypoint.sh;
}

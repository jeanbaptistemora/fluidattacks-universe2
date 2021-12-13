{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-subscriptions-daily-digest";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python39
      outputs."/integrates/cache"
      outputs."/integrates/db"
      outputs."/integrates/storage"
    ];
  };
  entrypoint = ./entrypoint.sh;
}

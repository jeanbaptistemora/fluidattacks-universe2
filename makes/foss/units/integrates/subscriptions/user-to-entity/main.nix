{ inputs
, makeScript
, outputs
, projectPath
, ...
}:
makeScript {
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  name = "integrates-subscriptions-user-to-entity";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python37
      outputs."/integrates/cache"
      outputs."/integrates/db"
      outputs."/integrates/storage"
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/subscriptions/user-to-entity/entrypoint.sh";
}

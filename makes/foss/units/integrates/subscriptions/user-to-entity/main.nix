{ inputs
, makeScript
, projectPath
, ...
}:
makeScript {
  replace = {
    __argIntegratesEnv__ = inputs.product.integrates-back-env;
  };
  name = "integrates-subscriptions-user-to-entity";
  searchPaths = {
    bin = [
      inputs.nixpkgs.python37
      inputs.product.integrates-db
      inputs.product.integrates-cache
      inputs.product.integrates-storage
    ];
  };
  entrypoint = projectPath "/makes/foss/units/integrates/subscriptions/user-to-entity/entrypoint.sh";
}

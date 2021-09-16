{ inputs
, makeScript
, ...
}:
makeScript {
  replace = {
    __argSetupIntegratesFrontDevRuntime__ =
      inputs.product.integrates-front-config-dev-runtime;
  };
  entrypoint = ./entrypoint.sh;
  name = "integrates-front";
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.nodejs
    ];
    source = [ inputs.product.integrates-front-config-dev-runtime-env ];
  };
}

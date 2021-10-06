{ inputs
, makeScript
, outputs
, ...
}:
makeScript {
  replace = {
    __argSetupIntegratesFrontDevRuntime__ =
      outputs."/integrates/front/config/dev-runtime";
  };
  entrypoint = ./entrypoint.sh;
  name = "integrates-front";
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.nodejs
    ];
    source = [ outputs."/integrates/front/config/dev-runtime-env" ];
  };
}

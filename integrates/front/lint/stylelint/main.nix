{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argSetupIntegratesFrontDevRuntime__ =
      outputs."/integrates/front/config/dev-runtime";
  };
  entrypoint = ./entrypoint.sh;
  name = "integrates-front-lint-stylelint";
  searchPaths = {
    bin = [inputs.nixpkgs.nodejs-18_x];
    source = [outputs."/integrates/front/config/dev-runtime-env"];
  };
}

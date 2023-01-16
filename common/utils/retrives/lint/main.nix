{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argSetupRetrievesDevRuntime__ =
      outputs."/common/utils/retrives/config/dev-runtime";
  };
  entrypoint = ./entrypoint.sh;
  name = "retrieves-lint-eslint";
  searchPaths = {
    bin = [inputs.nixpkgs.nodejs-18_x];
    source = [
      outputs."/common/utils/retrives/config/dev-runtime-env"
    ];
  };
}

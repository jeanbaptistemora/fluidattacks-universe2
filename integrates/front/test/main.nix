{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  entrypoint = ./entrypoint.sh;
  name = "integrates-front-test";
  replace = {
    __argRuntime__ = outputs."/integrates/front/config/dev-runtime";
  };
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.nodejs-18_x
    ];
    source = [outputs."/integrates/front/config/dev-runtime-env"];
  };
}

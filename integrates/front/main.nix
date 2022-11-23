{
  inputs,
  makeScript,
  outputs,
  ...
}:
makeScript {
  replace = {
    __argCertsDevelopment__ = outputs."/integrates/certs/dev";
    __argRuntime__ = outputs."/integrates/front/config/dev-runtime";
  };
  entrypoint = ./entrypoint.sh;
  name = "integrates-front";
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.nodejs-18_x
    ];
    source = [outputs."/integrates/front/config/dev-runtime-env"];
  };
}

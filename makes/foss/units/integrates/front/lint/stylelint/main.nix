{
  inputs,
  makeDerivation,
  outputs,
  projectPath,
  ...
}:
makeDerivation {
  env = {
    envSetupIntegratesFrontDevRuntime =
      outputs."/integrates/front/config/dev-runtime";
    envSrcIntegratesFront = projectPath "/integrates/front";
  };
  builder = ./builder.sh;
  name = "integrates-front-lint-stylelint";
  searchPaths = {
    bin = [inputs.nixpkgs.nodejs-14_x];
    source = [outputs."/integrates/front/config/dev-runtime-env"];
  };
}

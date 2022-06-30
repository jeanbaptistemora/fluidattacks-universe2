{
  inputs,
  makeDerivation,
  outputs,
  projectPath,
  ...
}:
makeDerivation {
  env = {
    envSetupIntegratesMobileDevRuntime =
      outputs."/integrates/mobile/config/dev-runtime";
    envSrcIntegratesMobile = projectPath "/integrates/mobile";
  };
  builder = ./builder.sh;
  name = "integrates-mobile-test-enzyme";
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.nodejs-14_x
    ];
    source = [outputs."/integrates/mobile/config/dev-runtime-env"];
  };
}

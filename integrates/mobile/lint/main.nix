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
  name = "integrates-mobile-lint";
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.nodejs-12_x
    ];
    source = [
      outputs."/common/utils/lint-typescript"
      outputs."/integrates/mobile/config/dev-runtime-env"
    ];
  };
}

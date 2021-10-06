{ inputs
, makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  env = {
    envSetupIntegratesMobileDevRuntime =
      outputs."/integrates/mobile/config/dev-runtime";
    envSrcIntegratesMobile = projectPath "/integrates/mobile";
  };
  builder = projectPath "/makes/foss/units/integrates/mobile/test/builder.sh";
  name = "integrates-mobile-test";
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.nodejs-12_x
    ];
    source = [ outputs."/integrates/mobile/config/dev-runtime-env" ];
  };
}

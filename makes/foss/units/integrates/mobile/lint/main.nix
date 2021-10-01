{ inputs
, makeDerivation
, projectPath
, ...
}:
makeDerivation {
  env = {
    envSetupIntegratesMobileDevRuntime =
      inputs.product.integrates-mobile-config-dev-runtime;
    envSrcIntegratesMobile = projectPath "/integrates/mobile";
  };
  builder = projectPath "/makes/foss/units/integrates/mobile/lint/builder.sh";
  name = "integrates-mobile-lint";
  searchPaths = {
    bin = [
      inputs.nixpkgs.bash
      inputs.nixpkgs.nodejs-12_x
    ];
    source = [
      inputs.product.integrates-mobile-config-dev-runtime-env
      (inputs.legacy.importUtility "lint-typescript")
    ];
  };
}

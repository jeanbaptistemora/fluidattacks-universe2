{ inputs
, makeDerivation
, projectPath
, ...
}:
makeDerivation {
  env = {
    envSetupIntegratesFrontDevRuntime =
      inputs.product.integrates-front-config-dev-runtime;
    envSrcIntegratesFront = projectPath "/integrates/front";
  };
  builder = projectPath "/makes/foss/units/integrates/front/lint/stylelint/builder.sh";
  name = "integrates-front-lint-stylelint";
  searchPaths = {
    bin = [ inputs.nixpkgs.nodejs ];
    source = [ inputs.product.integrates-front-config-dev-runtime-env ];
  };
}

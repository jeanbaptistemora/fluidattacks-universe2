{ inputs
, makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  env = {
    envSetupIntegratesFrontDevRuntime =
      outputs."/integrates/front/config/dev-runtime";
    envSrcIntegratesFront = projectPath "/integrates/front";
  };
  builder = projectPath "/makes/foss/units/integrates/front/lint/stylelint/builder.sh";
  name = "integrates-front-lint-stylelint";
  searchPaths = {
    bin = [ inputs.nixpkgs.nodejs ];
    source = [ outputs."/integrates/front/config/dev-runtime-env" ];
  };
}

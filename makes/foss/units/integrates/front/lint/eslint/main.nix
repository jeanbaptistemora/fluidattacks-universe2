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
  builder = projectPath "/makes/foss/units/integrates/front/lint/eslint/builder.sh";
  name = "integrates-front-lint-eslint";
  searchPaths = {
    bin = [ inputs.nixpkgs.nodejs ];
    source = [
      (inputs.legacy.importUtility "lint-typescript")
      outputs."/integrates/front/config/dev-runtime-env"
    ];
  };
}

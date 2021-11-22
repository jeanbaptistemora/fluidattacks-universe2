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
  builder = ./builder.sh;
  name = "integrates-front-lint-eslint";
  searchPaths = {
    bin = [ inputs.nixpkgs.nodejs ];
    source = [
      outputs."/utils/lint-typescript"
      outputs."/integrates/front/config/dev-runtime-env"
    ];
  };
}

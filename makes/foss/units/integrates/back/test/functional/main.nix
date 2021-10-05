{ inputs
, makePythonPypiEnvironment
, makeScript
, outputs
, ...
}:
let
  name = "integrates-back-test-functional";
  pythonRequirements = makePythonPypiEnvironment {
    inherit name;
    sourcesYaml = ./pypi-sources.yaml;
  };
in
makeScript {
  inherit name;
  replace = {
    __argIntegratesEnv__ = inputs.product.integrates-back-env;
  };
  searchPaths = {
    bin = [
      inputs.product.integrates-db
      inputs.product.integrates-storage
      outputs."/integrates/cache"
    ];
    source = [
      pythonRequirements
    ];
  };
  entrypoint = ./entrypoint.sh;
}

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
      outputs."/integrates/cache"
      outputs."/integrates/db"
      outputs."/integrates/storage"
    ];
    source = [
      pythonRequirements
    ];
  };
  entrypoint = ./entrypoint.sh;
}

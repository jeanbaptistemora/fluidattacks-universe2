{ makePythonPypiEnvironment
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
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
  };
  searchPaths = {
    bin = [
      outputs."/integrates/batch"
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

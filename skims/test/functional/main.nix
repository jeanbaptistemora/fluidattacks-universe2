{
  makePythonPypiEnvironment,
  makeScript,
  outputs,
  ...
}: let
  name = "skims-test-functional";
  pythonRequirements = makePythonPypiEnvironment {
    inherit name;
    sourcesYaml = ./sources-py.yaml;
  };
in
  makeScript {
    inherit name;
    searchPaths = {
      bin = [
        outputs."/integrates/cache"
        outputs."/integrates/db"
        outputs."/integrates/storage"
        outputs."/integrates/back"
      ];
      source = [
        outputs."/skims/config/runtime"
        outputs."/common/utils/sops"
        outputs."/secretsForAwsFromEnv/dev"
        pythonRequirements
      ];
    };
    entrypoint = ./entrypoint.sh;
  }

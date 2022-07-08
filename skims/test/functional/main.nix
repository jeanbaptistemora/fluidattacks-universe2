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
        outputs."/integrates/batch"
        outputs."/integrates/cache"
        outputs."/integrates/db"
        outputs."/integrates/storage"
        outputs."/skims"
      ];
      source = [
        outputs."/skims/config/runtime"
        outputs."/common/utils/sops"
        pythonRequirements
      ];
    };
    entrypoint = ./entrypoint.sh;
  }

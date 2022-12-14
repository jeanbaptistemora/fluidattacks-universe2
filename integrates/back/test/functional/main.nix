{
  inputs,
  makePythonPypiEnvironment,
  makeScript,
  outputs,
  ...
}: let
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
        inputs.nixpkgs.tokei
        outputs."/integrates/batch"
        outputs."/integrates/db"
      ];
      source = [
        outputs."/common/utils/sops"
        outputs."/integrates/storage/dev/lib/populate"
        pythonRequirements
      ];
    };
    entrypoint = ./entrypoint.sh;
  }

{
  inputs,
  makePythonPypiEnvironment,
  makeScript,
  outputs,
  projectPath,
  ...
}: let
  pythonEnvironment = makePythonPypiEnvironment {
    name = "integrates-streams-runtime";
    sourcesYaml = ./sources.yaml;
  };
in
  makeScript {
    entrypoint = ./entrypoint.sh;
    name = "integrates-streams";
    replace = {
      __argSecretsDev__ = projectPath "/integrates/secrets/development.yaml";
      __argSecretsProd__ = projectPath "/integrates/secrets/production.yaml";
    };
    searchPaths = {
      bin = [
        inputs.nixpkgs.python39
      ];
      source = [
        pythonEnvironment
        outputs."/common/utils/aws"
        outputs."/common/utils/sops"
      ];
    };
  }

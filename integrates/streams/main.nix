{
  inputs,
  makePythonPypiEnvironment,
  makeScript,
  outputs,
  ...
}: let
  pythonEnvironment = makePythonPypiEnvironment {
    name = "integrates-streams-runtime";
    sourcesYaml = ./sources.yaml;
  };
in
  makeScript {
    name = "integrates-streams";
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
    entrypoint = ./entrypoint.sh;
  }

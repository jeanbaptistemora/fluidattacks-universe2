{ makePythonPypiEnvironment
, makeScript
, outputs
, projectPath
, ...
}:
let
  name = "integrates-linth-python";
  pythonRequirements = makePythonPypiEnvironment {
    inherit name;
    sourcesYaml = ./mypy-sources.yaml;
  };
in
makeScript {
  inherit name;
  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
    __argIntegratesPackage__ = projectPath "/integrates/back/src";
  };
  searchPaths = {
    source = [
      pythonRequirements
    ];
  };
  entrypoint = ./entrypoint.sh;
}

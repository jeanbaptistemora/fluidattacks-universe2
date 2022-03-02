{ makePythonPypiEnvironment
, makeScript
, outputs
, projectPath
, __nixpkgs__
, ...
}:
let
  name = "integrates-lint-python";
  pythonRequirements = makePythonPypiEnvironment {
    inherit name;
    sourcesYaml = ./mypy-sources.yaml;
  };
in
makeScript {
  inherit name;
  searchPaths = {
    source = [
      pythonRequirements
    ];
    bin = [ __nixpkgs__.findutils ];
  };

  replace = {
    __argIntegratesBackEnv__ = outputs."/integrates/back/env";
    __argIntegratesPackage__ = projectPath "/integrates/back/src";
    __argSettingsMypy__ = projectPath "/makes/foss/units/integrates/back/lintPythonIso/settings-mypy.cfg";
  };

  entrypoint = ./entrypoint.sh;
}

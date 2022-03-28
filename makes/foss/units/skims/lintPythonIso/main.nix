{
  makePythonPypiEnvironment,
  makeScript,
  outputs,
  projectPath,
  __nixpkgs__,
  ...
}: let
  name = "skims-lint-python";
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
        outputs."/skims/config-runtime"
      ];
      bin = [__nixpkgs__.findutils];
    };

    replace = {
      __argSkimsPackage__ = projectPath "/skims/skims/";
      __argSettingsMypy__ = projectPath "/makes/foss/units/skims/lintPythonIso/settings-mypy.cfg";
    };

    entrypoint = ./entrypoint.sh;
  }

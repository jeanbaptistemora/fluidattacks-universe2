{
  inputs,
  makePythonPypiEnvironment,
  makeTemplate,
  projectPath,
  ...
}:
makeTemplate {
  replace = {
    __argSrcForces__ = projectPath "/forces";
  };
  name = "forces-config-runtime";
  searchPaths = {
    bin = [
      inputs.nixpkgs.git
      inputs.nixpkgs.python38
    ];
    pythonMypy = [
      (projectPath "/forces")
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "forces-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
    pythonPackage = [
      (projectPath "/common/bugsnag/client")
      (projectPath "/forces")
    ];
  };
  template = ./template.sh;
}

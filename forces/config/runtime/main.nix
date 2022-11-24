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
    ];
    source = [
      (makePythonPypiEnvironment {
        name = "forces-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
    pythonPackage = [
      (projectPath "/common/utils/bugsnag/client")
      (projectPath "/forces")
    ];
  };
  template = ./template.sh;
}

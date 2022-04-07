{
  makePythonPypiEnvironment,
  makeTemplate,
  ...
}:
makeTemplate {
  name = "common-python-safe-pickle";
  searchPaths = {
    pythonPackage = [./src];
    source = [
      (makePythonPypiEnvironment {
        name = "common-python-safe-pickle";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}

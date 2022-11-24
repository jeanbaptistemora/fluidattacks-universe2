{
  makePythonPypiEnvironment,
  makeTemplate,
  ...
}:
makeTemplate {
  name = "common-python-serializers";
  searchPaths = {
    pythonPackage = [./src];
    source = [
      (makePythonPypiEnvironment {
        name = "common-python-serializers";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}

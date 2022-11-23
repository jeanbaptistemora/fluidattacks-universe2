{
  makePythonPypiEnvironment,
  makeTemplate,
  projectPath,
  ...
}:
makeTemplate {
  name = "integrates-back-charts";
  searchPaths = {
    source = [
      (makePythonPypiEnvironment {
        name = "integrates-back-charts-pypi";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
    pythonPackage = [
      (projectPath "/integrates/charts")
    ];
  };
}

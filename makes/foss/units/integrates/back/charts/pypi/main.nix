{ makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
makeTemplate {
  name = "integrates-back-charts";
  searchPaths = {
    pythonMypy = [
      (projectPath "/integrates/charts")
    ];
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

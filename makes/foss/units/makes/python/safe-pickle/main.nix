{ makePythonPypiEnvironment
, makeTemplate
, ...
}:
makeTemplate {
  name = "makes-python-safe-pickle";
  searchPaths = {
    pythonPackage = [ ./src ];
    source = [
      (makePythonPypiEnvironment {
        name = "makes-python-safe-pickle";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}

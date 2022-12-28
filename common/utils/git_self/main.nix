{
  makePythonPypiEnvironment,
  makeTemplate,
  ...
}:
makeTemplate {
  name = "common-python-git-self";
  searchPaths = {
    pythonPackage = [./src];
    source = [
      (makePythonPypiEnvironment {
        name = "common-python-git-self";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}

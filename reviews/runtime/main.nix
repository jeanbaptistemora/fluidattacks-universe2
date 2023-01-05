{
  makePythonPypiEnvironment,
  makePythonVersion,
  makeTemplate,
  projectPath,
  ...
}:
makeTemplate {
  replace = {
    __argSrcReviews__ = projectPath "/reviews/src";
  };
  name = "reviews-runtime";
  searchPaths = {
    bin = [(makePythonVersion "3.11")];
    pythonPackage = [(projectPath "/reviews/src")];
    source = [
      (makePythonPypiEnvironment {
        name = "reviews-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
  template = ./template.sh;
}

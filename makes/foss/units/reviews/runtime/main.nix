{ inputs
, makePythonPypiEnvironment
, makeTemplate
, outputs
, projectPath
, ...
}:
makeTemplate {
  replace = {
    __argSrcReviews__ = projectPath "/reviews/src";
  };
  name = "reviews-runtime";
  searchPaths = {
    bin = [ inputs.nixpkgs.python38 ];
    pythonPackage = [ (projectPath "/reviews/src") ];
    source = [
      (makePythonPypiEnvironment {
        name = "reviews-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
      outputs."/makes/commitlint"
    ];
  };
  template = ./template.sh;
}

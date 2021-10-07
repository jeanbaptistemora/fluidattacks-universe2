{ inputs
, makePythonPypiEnvironment
, makeTemplate
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
      (inputs.product.makes-commitlint)
      (makePythonPypiEnvironment {
        name = "reviews-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
  template = ./template.sh;
}

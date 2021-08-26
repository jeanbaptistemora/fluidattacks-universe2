{ makes
, makeTemplate
, packages
, path
, nixpkgs
, ...
}:
makeTemplate {
  arguments = {
    envSrcReviews = path "/reviews/src";
  };
  name = "reviews-runtime";
  searchPaths = {
    envPaths = [
      nixpkgs.python38
    ];
    envPythonPaths = [
      (path "/reviews/src")
    ];
    envNodeBinaries = [
      packages.makes.commitlint
    ];
    envNodeLibraries = [
      packages.makes.commitlint
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "reviews-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
  template = path "/makes/packages/reviews/runtime/template.sh";
}

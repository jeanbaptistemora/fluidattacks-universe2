{ makes
, makeTemplate
, nixpkgs
, path
, ...
}:
makeTemplate {
  arguments = {
    envSrcForces = path "/forces";
  };
  name = "forces-config-runtime";
  searchPaths = {
    envPaths = [
      nixpkgs.git
      nixpkgs.python38
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "forces-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
    envPythonPaths = [
      (path "/forces")
    ];
  };
  template = path "/makes/packages/forces/config-runtime/template.sh";
}

{ makes
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/tap_git";
in
makeTemplate {
  name = "observes-env-tap-git-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      nixpkgs.git
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-tap-git-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}

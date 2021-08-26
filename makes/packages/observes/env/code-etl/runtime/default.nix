{ makes
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  self = path "/observes/code_etl";
in
makeTemplate {
  name = "observes-env-code-etl-runtime";
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
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-code-etl-runtime";
        sourcesYaml = ./pypi-sources.yaml;
      })
    ];
  };
}

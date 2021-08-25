{ makes
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/common/postgres_client";
in
makeTemplate {
  name = "observes-env-postgres-client-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      nixpkgs.postgresql
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      (makes.makePythonPypiEnvironment {
        name = "observes-env-postgres-client-development";
        searchPaths.bin = [ nixpkgs.gcc nixpkgs.postgresql ];
        sourcesYaml = ./pypi-sources.yaml;
      })
      utils-logger.runtime
    ];
  };
}

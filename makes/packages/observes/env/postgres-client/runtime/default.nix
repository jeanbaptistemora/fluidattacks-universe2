{ makeTemplate
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
      postgres-client.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
      postgres-client.runtime.python
    ];
  };
}

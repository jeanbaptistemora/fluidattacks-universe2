{ makeTemplate
, nixpkgs
, path
, ...
}:
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
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
    ];
  };
}

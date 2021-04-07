{ makeTemplate
, nixpkgs
, path
, ...
}:
let
  self = path "/observes/common/postgres_client";
in
makeTemplate {
  name = "observes-env-runtime-postgres-client";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      nixpkgs.postgresql
      nixpkgs.python38Packages.psycopg2
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
    ];
  };
}

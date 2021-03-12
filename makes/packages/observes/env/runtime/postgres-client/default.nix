{ buildPythonPackage
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  self = buildPythonPackage {
    name = "observes-postgres-client";
    packagePath = path "/observes/common/postgres_client";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-runtime-postgres-client";
  searchPaths = {
    envPaths = [
      nixpkgs.postgresql
      nixpkgs.python38Packages.psycopg2
      self
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
      self
    ];
  };
}

{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  postgresClient = buildPythonPackage {
    name = "observes-postgres-client";
    packagePath = path "/observes/common/postgres_client";
    python = nixpkgs.python38;
  };
  self = buildPythonPackage {
    name = "observes-service-migrate-tables";
    packagePath = path "/observes/services/migrate_tables";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-service-migrate-tables-runtime";
  searchPaths = {
    envPaths = [
      nixpkgs.python38Packages.psycopg2
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
      packages.observes.env.service-migrate-tables.runtime.python
      postgresClient
      self
    ];
  };
}

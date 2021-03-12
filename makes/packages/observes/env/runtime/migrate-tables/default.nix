{ buildPythonPackage
, buildPythonRequirements
, makeTemplate
, nixpkgs
, path
, ...
}:
let
  pythonRequirements = buildPythonRequirements {
    name = "observes-env-runtime-migrate-tables-python";
    requirements = {
      direct = [
        "click==7.1.2"
      ];
      inherited = [ ];
    };
    python = nixpkgs.python38;
  };
  postgresClient = buildPythonPackage {
    name = "observes-postgres-client";
    packagePath = path "/observes/common/postgres_client";
    python = nixpkgs.python38;
  };
  self = buildPythonPackage {
    name = "observes-migrate-tables";
    packagePath = path "/observes/services/migrate_tables";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-runtime-migrate-tables";
  searchPaths = {
    envPaths = [
      postgresClient
      pythonRequirements
      self
    ];
    envPython38Paths = [
      postgresClient
      pythonRequirements
      self
    ];
  };
}

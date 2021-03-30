{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  pkgEnv = packages.observes.env.streamer-zoho-crm;
  pythonRunReqs = pkgEnv.runtime.python;
  postgresClient = buildPythonPackage {
    name = "observes-streamer-zoho-crm";
    packagePath = path "/observes/common/postgres_client";
    python = nixpkgs.python38;
  };
  singerIO = buildPythonPackage {
    name = "observes-singer-io";
    packagePath = path "/observes/common/singer_io";
    python = nixpkgs.python38;
  };
  self = buildPythonPackage {
    name = "observes-streamer-zoho-crm";
    packagePath = path "/observes/singer/streamer_zoho_crm";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-streamer-zoho-crm-runtime";
  searchPaths = {
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
      pythonRunReqs
      postgresClient
      singerIO
      self
    ];
  };
}

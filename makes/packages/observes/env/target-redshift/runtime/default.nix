{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  pkgEnv = packages.observes.env;
  self = buildPythonPackage {
    name = "observes-streamer-zoho-crm";
    packagePath = path "/observes/singer/streamer_zoho_crm";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-runtime-streamer-zoho-crm";
  searchPaths = {
    envSources = [
      pkgEnv.runtime.singer-io
      pkgEnv.runtime.postgres-client
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
      self
    ];
  };
}

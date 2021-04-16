{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.streamer-zoho-crm;
  self = buildPythonPackage {
    name = "observes-streamer-zoho-crm";
    packagePath = path "/observes/singer/streamer_zoho_crm";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-streamer-zoho-crm-runtime";
  searchPaths = {
    envPaths = [
      pkgEnv.runtime.python
    ];
    envSources = [
      env.postgres-client.runtime
      env.singer-io.runtime
      env.utils-logger.runtime
    ];
    envPython38Paths = [
      pkgEnv.runtime.python
      self
    ];
  };
}

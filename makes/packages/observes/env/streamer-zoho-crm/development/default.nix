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
  name = "observes-env-streamer-zoho-crm-development";
  searchPaths = {
    envSources = [
      pkgEnv.runtime
    ];
    envPaths = [
      pkgEnv.development.python
    ];
    envPython38Paths = [
      pkgEnv.development.python
      self
    ];
    envMypy38Paths = [
      self
    ];
  };
}

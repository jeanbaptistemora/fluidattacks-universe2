{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.tap-mixpanel;
  self = buildPythonPackage {
    name = "observes-tap-mixpanel";
    packagePath = path "/observes/singer/tap_mixpanel";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-tap-mixpanel-development";
  searchPaths = {
    envPaths = [
      pkgEnv.development.python
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.pandas
      pkgEnv.development.python
      self
    ];
    envSources = [
      env.runtime.singer-io
    ];
  };
}

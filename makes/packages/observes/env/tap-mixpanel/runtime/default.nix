{ makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.tap-mixpanel;
  self = path "/observes/singer/tap_mixpanel";
in
makeTemplate {
  name = "observes-env-tap-mixpanel-runtime";
  searchPaths = {
    envPaths = [
      pkgEnv.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.pandas
      pkgEnv.runtime.python
    ];
    envSources = [
      env.runtime.singer-io
    ];
  };
}

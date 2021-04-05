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
  name = "observes-env-tap-mixpanel-runtime";
  searchPaths = {
    envPaths = [
      pkgEnv.runtime.python
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.pandas
      pkgEnv.runtime.python
      self
    ];
    envSources = [
      env.runtime.singer-io
    ];
  };
}

{ makeTemplate
, packages
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.tap-mixpanel;
in
makeTemplate {
  name = "observes-env-tap-mixpanel-development";
  searchPaths = {
    envPaths = [
      pkgEnv.development.python
    ];
    envPython38Paths = [
      pkgEnv.development.python
    ];
    envSources = [
      pkgEnv.runtime
    ];
  };
}

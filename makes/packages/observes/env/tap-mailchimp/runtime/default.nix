{ makeTemplate
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.tap-mailchimp;
  self = path "/observes/singer/tap_mailchimp";
in
makeTemplate {
  name = "observes-env-tap-mailchimp-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      pkgEnv.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      pkgEnv.runtime.python
    ];
    envSources = [
      env.singer-io.runtime
      env.paginator.runtime
      env.utils-logger.runtime
    ];
  };
}

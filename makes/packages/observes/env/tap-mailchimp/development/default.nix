{ makeTemplate
, packages
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.tap-mailchimp;
in
makeTemplate {
  name = "observes-env-tap-mailchimp-development";
  searchPaths = {
    envPython38Paths = [
      pkgEnv.development.python
    ];
    envSources = [
      pkgEnv.runtime
    ];
  };
}

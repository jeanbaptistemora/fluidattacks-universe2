{ makeTemplate
, packages
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.target-redshift;
in
makeTemplate {
  name = "observes-env-target-redshift-development";
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

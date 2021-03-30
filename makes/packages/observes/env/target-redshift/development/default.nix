{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  pkgEnv = env.target-redshift;
  self = buildPythonPackage {
    name = "observes-target-redshift";
    packagePath = path "/observes/singer/target_redshift_2";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-target-redshift-development";
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

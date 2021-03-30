{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  pkgEnv = packages.observes.env.target-redshift;
  pythonDevReqs = pkgEnv.development.python;
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
      packages.observes.env.runtime.singer-io
      packages.observes.env.runtime.postgres-client
    ];
    envPaths = [
      pythonDevReqs
    ];
    envPython38Paths = [
      pythonDevReqs
      self
    ];
    envMypy38Paths = [
      self
    ];
  };
}

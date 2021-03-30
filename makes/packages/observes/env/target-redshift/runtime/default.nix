{ buildPythonPackage
, makeTemplate
, nixpkgs
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  self = buildPythonPackage {
    name = "observes-target-redshift";
    packagePath = path "/observes/singer/target_redshift_2";
    python = nixpkgs.python38;
  };
in
makeTemplate {
  name = "observes-env-target-redshift-runtime";
  searchPaths = {
    envSources = [
      env.runtime.singer-io
      env.runtime.postgres-client
    ];
    envPython38Paths = [
      nixpkgs.python38Packages.psycopg2
      self
    ];
  };
}

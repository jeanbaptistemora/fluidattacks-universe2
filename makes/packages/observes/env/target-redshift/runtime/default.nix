{ makeTemplate
, packages
, path
, ...
}:
let
  env = packages.observes.env;
  self = path "/observes/singer/target_redshift_2";
in
makeTemplate {
  name = "observes-env-target-redshift-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      env.singer-io.runtime
      env.postgres-client.runtime
    ];
  };
}

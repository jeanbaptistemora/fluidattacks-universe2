{ makeTemplate
, packages
, path
, ...
}:
let
  self = path "/observes/singer/target_redshift";
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
      packages.observes.env.target-redshift.runtime.python
      packages.observes.env.postgres-client.runtime
      packages.observes.env.singer-io.runtime
      packages.observes.env.utils-logger.runtime
    ];
  };
}

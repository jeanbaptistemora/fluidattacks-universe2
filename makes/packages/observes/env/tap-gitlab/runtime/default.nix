{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/streamer_gitlab";
in
makeTemplate {
  name = "observes-env-tap-gitlab-runtime";
  searchPaths = {
    envPaths = [
      tap-gitlab.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      tap-gitlab.runtime.python
    ];
    envSources = [
      paginator.runtime
      postgres-client.runtime
      singer-io.runtime
      utils-logger.runtime
    ];
  };
}

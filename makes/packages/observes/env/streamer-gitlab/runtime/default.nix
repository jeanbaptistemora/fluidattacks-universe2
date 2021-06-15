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
  name = "observes-env-streamer-gitlab-runtime";
  searchPaths = {
    envPaths = [
      streamer-gitlab.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      streamer-gitlab.runtime.python
    ];
    envSources = [
      paginator.runtime
      postgres-client.runtime
      singer-io.runtime
      utils-logger.runtime
    ];
  };
}

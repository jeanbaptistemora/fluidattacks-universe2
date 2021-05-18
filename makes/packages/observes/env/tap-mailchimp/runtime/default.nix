{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/tap_mailchimp";
in
makeTemplate {
  name = "observes-env-tap-mailchimp-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      tap-mailchimp.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      tap-mailchimp.runtime.python
    ];
    envSources = [
      singer-io.runtime
      paginator.runtime
      utils-logger.runtime
    ];
  };
}

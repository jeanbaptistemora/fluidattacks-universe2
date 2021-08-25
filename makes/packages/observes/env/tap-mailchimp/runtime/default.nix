{ makeTemplate
, packages
, path
, ...
}:
let
  self = path "/observes/singer/tap_mailchimp";
in
makeTemplate {
  name = "observes-env-tap-mailchimp-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPythonPaths = [
      self
    ];
    envSources = [
      packages.observes.env.tap-mailchimp.runtime.python
      packages.observes.env.singer-io.runtime
      packages.observes.env.paginator.runtime
      packages.observes.env.utils-logger.runtime
    ];
  };
}

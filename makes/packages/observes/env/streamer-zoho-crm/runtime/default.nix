{ makeTemplate
, packages
, path
, ...
}:
with packages.observes.env;
let
  self = path "/observes/singer/streamer_zoho_crm";
in
makeTemplate {
  name = "observes-env-streamer-zoho-crm-runtime";
  searchPaths = {
    envMypyPaths = [
      self
    ];
    envPaths = [
      streamer-zoho-crm.runtime.python
    ];
    envPythonPaths = [
      self
    ];
    envPython38Paths = [
      streamer-zoho-crm.runtime.python
    ];
    envSources = [
      postgres-client.runtime
      singer-io.runtime
      utils-logger.runtime
    ];
  };
}

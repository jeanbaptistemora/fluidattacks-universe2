{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-streamer-zoho-crm-development";
  searchPaths = {
    envPaths = [
      streamer-zoho-crm.development.python
    ];
    envPython38Paths = [
      streamer-zoho-crm.development.python
    ];
    envSources = [
      streamer-zoho-crm.runtime
    ];
    envUtils = [
      "/makes/utils/lint-python"
    ];
  };
}

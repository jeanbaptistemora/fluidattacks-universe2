{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-tap-mailchimp-development";
  searchPaths = {
    envPython38Paths = [
      tap-mailchimp.development.python
    ];
    envSources = [
      tap-mailchimp.runtime
    ];
    envUtils = [
      "/makes/utils/lint-python"
    ];
  };
}

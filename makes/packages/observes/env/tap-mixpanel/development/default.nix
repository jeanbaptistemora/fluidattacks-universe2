{ makeTemplate
, packages
, ...
}:
with packages.observes.env;
makeTemplate {
  name = "observes-env-tap-mixpanel-development";
  searchPaths = {
    envPaths = [
      tap-mixpanel.development.python
    ];
    envPython38Paths = [
      tap-mixpanel.development.python
    ];
    envSources = [
      tap-mixpanel.runtime
    ];
  };
}

{ makeTemplate
, packages
, ...
}:
makeTemplate {
  name = "observes-env-tap-bugsnag-development";
  searchPaths = {
    envSources = [
      packages.observes.env.tap-bugsnag.runtime
    ];
  };
}

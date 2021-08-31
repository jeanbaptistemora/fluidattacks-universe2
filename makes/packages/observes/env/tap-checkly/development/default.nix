{ makeTemplate
, packages
, ...
}:
makeTemplate {
  name = "observes-env-tap-checkly-development";
  searchPaths = {
    envSources = [
      packages.observes.env.tap-checkly.runtime
    ];
  };
}

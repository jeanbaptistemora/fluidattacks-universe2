{ makeTemplate
, packages
, ...
}:
makeTemplate {
  name = "observes-env-tap-json-development";
  searchPaths = {
    envSources = [
      packages.observes.env.tap-json.runtime
    ];
  };
}

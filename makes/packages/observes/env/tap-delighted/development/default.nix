{ makeTemplate
, packages
, ...
}:
makeTemplate {
  name = "observes-env-tap-delighted-development";
  searchPaths = {
    envSources = [
      packages.observes.env.tap-delighted.runtime
    ];
  };
}

{ makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  name = "makes-dev-observes-tap-mixpanel";
  searchPaths = {
    envSources = [
      packages.observes.env.tap-mixpanel.development
      packages.observes.env.tap-mixpanel.runtime
    ];
  };
  template = path "/makes/packages/makes/dev/observes/tap-mixpanel/template.sh";
}

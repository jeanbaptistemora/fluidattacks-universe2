{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from tap_mixpanel import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.tap-mixpanel.runtime
    ];
  };
  name = "observes-bin-tap-mixpanel";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}

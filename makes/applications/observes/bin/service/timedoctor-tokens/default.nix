{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from timedoctor_tokens import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.service-timedoctor-tokens.runtime
    ];
  };
  name = "observes-bin-service-timedoctor-tokens";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}

{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from batch_stability import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.service-batch-stability.runtime
    ];
  };
  name = "observes-bin-service-batch-stability";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}

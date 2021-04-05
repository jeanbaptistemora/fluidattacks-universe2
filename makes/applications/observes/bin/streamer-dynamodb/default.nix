{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from streamer_dynamodb import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.streamer-dynamodb.runtime
    ];
  };
  name = "observes-bin-streamer-dynamodb";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}

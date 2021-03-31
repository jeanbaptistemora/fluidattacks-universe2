{ makeEntrypoint
, nixpkgs
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from streamer_dynamodb import main";
  };
  searchPaths = {
    envPaths = [
      nixpkgs.python38
    ];
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.runtime.streamer-dynamodb
    ];
  };
  name = "observes-bin-streamer-dynamodb";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}

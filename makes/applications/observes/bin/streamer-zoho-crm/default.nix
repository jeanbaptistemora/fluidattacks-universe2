{ makeEntrypoint
, nixpkgs
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from streamer_zoho_crm.cli import main";
  };
  searchPaths = {
    envPaths = [
      nixpkgs.python38
    ];
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.streamer-zoho-crm.runtime
    ];
  };
  name = "observes-bin-streamer-zoho-crm";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}

{ makeEntrypoint
, nixpkgs
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from tap_mailchimp.cli import main";
  };
  searchPaths = {
    envPaths = [
      nixpkgs.python38
    ];
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.tap-mailchimp.runtime
    ];
  };
  name = "observes-bin-tap-mailchimp";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}

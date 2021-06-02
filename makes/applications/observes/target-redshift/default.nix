{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from target_redshift.cli import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.target-redshift.runtime
    ];
  };
  name = "observes-target-redshift";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}

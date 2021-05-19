{ makeEntrypoint
, packages
, path
, ...
}:
makeEntrypoint {
  arguments = {
    envEntrypoint = "from dif_gitlab_etl.cli import main";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.runner
      packages.observes.env.gitlab-etl.runtime
    ];
  };
  name = "observes-bin-dif-gitlab-etl";
  template = path "/makes/packages/observes/generic/runner/runner_entrypoint.sh";
}

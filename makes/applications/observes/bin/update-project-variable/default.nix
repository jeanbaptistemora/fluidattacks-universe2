{ makeEntrypoint
, path
, ...
}:
makeEntrypoint {
  searchPaths = {
    envUtils = [
      "/makes/utils/gitlab"
    ];
  };
  name = "observes-bin-update-project-variable";
  template = path "/makes/applications/observes/bin/update-project-variable/entrypoint.sh";
}

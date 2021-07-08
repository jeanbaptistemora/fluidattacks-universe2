{ makeEntrypoint
, path
, packages
, ...
}:
makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.bin.tap-gitlab
      packages.observes.tap-json
      packages.observes.target-redshift
    ];
  };
  name = "observes-job-gitlab-etl";
  template = path "/makes/applications/observes/job/gitlab-etl/entrypoint.sh";
}

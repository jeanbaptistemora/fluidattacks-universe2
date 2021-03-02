{ path, packages, ... } @ attrs:
let
  observes = import (path "/makes/libs/observes") attrs;
in
observes.makeUtils.makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.dif-gitlab-etl
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-job-dif-gitlab-etl";
  template = path "/makes/applications/observes/job/dif-gitlab-etl/entrypoint.sh";
}

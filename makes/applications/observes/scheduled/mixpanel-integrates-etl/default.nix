{ path, packages, ... } @ attrs:
let
  observes = import (path "/makes/libs/observes") attrs;
in
observes.makeUtils.makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.tap-json
      packages.observes.tap-mixpanel
      packages.observes.target-redshift
      packages.observes.update-sync-date
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-mixpanel-integrates-etl";
  template = path "/makes/applications/observes/scheduled/mixpanel-integrates-etl/entrypoint.sh";
}

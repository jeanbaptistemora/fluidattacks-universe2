{ path, packages, ... } @ attrs:
let
  observes = import (path "/makes/libs/observes") attrs;
in
observes.makeUtils.makeEntrypoint {
  searchPaths = {
    envPaths = [
      packages.observes.target-redshift
      packages.observes.tap-json
      packages.observes.tap-mailchimp

    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  name = "observes-scheduled-mailchimp-etl";
  template = path "/makes/applications/observes/scheduled/mailchimp-etl/entrypoint.sh";
}

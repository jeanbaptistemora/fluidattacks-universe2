{ applications
, observesPkgs
, path
, ...
}:
let
  nixPkgs = observesPkgs;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixPkgs;
in
makeEntrypoint {
  arguments = {
    envTapJson = applications.observes.tap-json;
    envTapMixpanel = applications.observes.tap-mixpanel;
    envTargetRedshift = applications.observes.target-redshift;
    envUpdateSyncDate = applications.observes.update-sync-date;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path nixPkgs;
  };
  name = "observes-scheduled-mixpanel-integrates-etl";
  template = path "/makes/applications/observes/scheduled/mixpanel-integrates-etl/entrypoint.sh";
}

{ observesPkgs
, applications
, path
, ...
} @ _:
let
  nixPkgs = observesPkgs;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixPkgs;
in
makeEntrypoint {
  arguments = {
    envTapFormstack = applications.observes.tap-formstack;
    envTargetRedshift = applications.observes.target-redshift;
    envUpdateSyncDate = applications.observes.update-sync-date;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path nixPkgs;
  };
  name = "observes-scheduled-formstack-etl";
  template = path "/makes/applications/observes/scheduled/formstack-etl/entrypoint.sh";
}

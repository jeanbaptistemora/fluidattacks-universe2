{ applications
, observesPkgs
, path
, ...
} @ _:
let
  nixPkgs = observesPkgs;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixPkgs;
in
makeEntrypoint {
  arguments = {
    envStreamerZohoCrm = applications."observes/streamer-zoho-crm";
    envTapCsv = applications."observes/tap-csv";
    envTapJson = applications."observes/tap-json";
    envTargetRedshift = applications."observes/target-redshift";
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path nixPkgs;
  };
  name = "observes-scheduled-zoho-crm-etl";
  template = path "/makes/applications/observes/scheduled-zoho-crm-etl/entrypoint.sh";
}

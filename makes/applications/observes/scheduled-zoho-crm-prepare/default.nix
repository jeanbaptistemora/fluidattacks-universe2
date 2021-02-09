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
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path nixPkgs;
  };
  name = "observes-scheduled-zoho-crm-prepare";
  template = path "/makes/applications/observes/scheduled-zoho-crm-prepare/entrypoint.sh";
}

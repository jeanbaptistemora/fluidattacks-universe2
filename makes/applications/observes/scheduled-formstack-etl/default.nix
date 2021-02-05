{ observesPkgs
, outputs
, path
, ...
} @ _:
let
  nixPkgs = observesPkgs;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixPkgs;
in
makeEntrypoint {
  arguments = {
    envTapFormstack = outputs.apps."observes/tap-formstack".program;
    envTargetRedshift = outputs.apps."observes/target-redshift".program;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path nixPkgs;
  };
  name = "observes-scheduled-formstack-etl";
  template = path "/makes/applications/observes/scheduled-formstack-etl/entrypoint.sh";
}

{ observesPkgs
, outputs
, path
, ...
} @ _:
let
  bins = import (path "/makes/libs/observes/bins") {
    inherit path;
    nixPkgs = observesPkgs;
  };
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path observesPkgs;
in
makeEntrypoint {
  arguments = {
    envMelts = outputs.apps.melts.program;
    envUpdateSyncDateBin = "${bins.updateSyncDate}/bin";
    envUtilsBashLibAws = import (path "/makes/utils/aws") path observesPkgs;
    envUtilsBashLibGit = import (path "/makes/utils/use-git-repo") path observesPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path observesPkgs;
  };
  name = "observes-code-etl-mirror";
  template = path "/makes/applications/observes/code-etl-mirror/entrypoint.sh";
}

{ observesPkgs
, applications
, path
, ...
} @ _:
let
  nixPkgs = observesPkgs;
  bins = import (path "/makes/libs/observes/bins") {
    inherit path nixPkgs;
  };
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixPkgs;
in
makeEntrypoint {
  arguments = {
    envMelts = applications.melts;
    envFindUtils = "${nixPkgs.findutils}/bin";
    envOpenSSH = "${nixPkgs.openssh}/bin";
    envSopsBin = "${nixPkgs.sops}/bin";
    envUpdateSyncDateBin = "${bins.updateSyncDate}/bin";
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixPkgs;
    envUtilsBashLibGit = import (path "/makes/utils/use-git-repo") path nixPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path nixPkgs;
  };
  name = "observes-code-etl-mirror";
  template = path "/makes/applications/observes/code-etl-mirror/entrypoint.sh";
}

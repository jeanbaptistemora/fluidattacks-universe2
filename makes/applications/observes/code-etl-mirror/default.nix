{ observesPkgs
, applications
, path
, ...
}:
let
  nixPkgs = observesPkgs;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixPkgs;
in
makeEntrypoint {
  arguments = {
    envMelts = applications.melts;
    envFindUtils = "${nixPkgs.findutils}/bin";
    envOpenSSH = "${nixPkgs.openssh}/bin";
    envSopsBin = "${nixPkgs.sops}/bin";
    envUpdateSyncDate = applications.observes.update-sync-date;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixPkgs;
    envUtilsBashLibGit = import (path "/makes/utils/git") path nixPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path nixPkgs;
  };
  name = "observes-code-etl-mirror";
  template = path "/makes/applications/observes/code-etl-mirror/entrypoint.sh";
}

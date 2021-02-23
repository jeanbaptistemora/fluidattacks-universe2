{ observesPkgs
, applications
, path
, ...
}:
let
  bins = import (path "/makes/libs/observes/bins") {
    inherit path;
    nixPkgs = observesPkgs;
  };
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path observesPkgs;
in
makeEntrypoint {
  arguments = {
    envCodeEtlBin = "${bins.codeEtl}/bin";
    envMelts = applications.melts;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path observesPkgs;
    envUtilsBashLibGit = import (path "/makes/utils/use-git-repo") path observesPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path observesPkgs;
  };
  name = "observes-code-etl-upload";
  template = path "/makes/applications/observes/code-etl-upload/entrypoint.sh";
}

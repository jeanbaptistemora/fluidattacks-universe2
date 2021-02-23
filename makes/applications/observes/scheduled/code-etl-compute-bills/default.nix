{ observesPkgs
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
    envUtilsBashLibAws = import (path "/makes/utils/aws") path observesPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path observesPkgs;
  };
  name = "observes-scheduled-code-etl-compute-bills";
  template = path "/makes/applications/observes/scheduled/code-etl-compute-bills/entrypoint.sh";
}

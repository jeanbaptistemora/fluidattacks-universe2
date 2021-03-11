{ nixpkgs
, path
, ...
}:
let
  bins = import (path "/makes/libs/observes/bins") {
    inherit path;
    nixPkgs = nixpkgs;
  };
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envCodeEtlBin = "${bins.codeEtl}/bin";
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixpkgs;
    envUtilsBashLibGit = import (path "/makes/utils/git") path nixpkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path nixpkgs;
  };
  name = "observes-scheduled-job-code-etl-amend";
  template = path "/makes/applications/observes/scheduled/job/code-etl-amend/entrypoint.sh";
}

{ nixpkgs2
, path
, ...
}:
let
  bins = import (path "/makes/libs/observes/bins") {
    inherit path;
    nixPkgs = nixpkgs2;
  };
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs2;
in
makeEntrypoint {
  arguments = {
    envCodeEtlBin = "${bins.codeEtl}/bin";
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixpkgs2;
    envUtilsBashLibGit = import (path "/makes/utils/git") path nixpkgs2;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path nixpkgs2;
  };
  name = "observes-code-etl-amend";
  template = path "/makes/applications/observes/code-etl-amend/entrypoint.sh";
}

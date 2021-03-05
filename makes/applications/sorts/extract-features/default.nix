{ packages
, path
, nixpkgs
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path nixpkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSortsRuntime = packages.sorts.config-runtime;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path nixpkgs;
    envUtilsBashLibGit = import (path "/makes/utils/git") path nixpkgs;
    envUtilsMeltsLibCommon = packages.melts.lib;
  };
  name = "sorts-extract-features";
  template = path "/makes/applications/sorts/extract-features/entrypoint.sh";
}

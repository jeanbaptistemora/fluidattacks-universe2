{ packages
, path
, sortsPkgs
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSortsRuntime = packages.sorts.config-runtime;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path sortsPkgs;
    envUtilsBashLibGit = import (path "/makes/utils/use-git-repo") path sortsPkgs;
    envUtilsMeltsLibCommon = packages.melts.lib;
  };
  name = "sorts-extract-features";
  template = path "/makes/applications/sorts/extract-features/entrypoint.sh";
}

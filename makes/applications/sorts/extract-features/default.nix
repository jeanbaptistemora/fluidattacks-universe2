{ path
, sortsPkgs
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSortsRuntime = import (path "/makes/packages/sorts/config-runtime") attrs.copy;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path sortsPkgs;
    envUtilsBashLibGit = import (path "/makes/utils/use-git-repo") path sortsPkgs;
    envUtilsMeltsLibCommon = import (path "/makes/libs/melts") attrs.copy;
  };
  name = "sorts-extract-features";
  template = path "/makes/applications/sorts/extract-features/entrypoint.sh";
}

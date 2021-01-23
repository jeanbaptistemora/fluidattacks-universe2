{ path
, sortsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/sorts/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSortsRuntime = config.setupSortsRuntime;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path sortsPkgs;
    envUtilsBashLibGit = import (path "/makes/utils/use-git-repo") path sortsPkgs;
    envUtilsMeltsLibCommon = import (path "/makes/utils/melts-lib") attrs.copy;
  };
  location = "/bin/sorts-extract-features";
  name = "sorts-extract-features";
  template = path "/makes/sorts/extract-features/entrypoint.sh";
}

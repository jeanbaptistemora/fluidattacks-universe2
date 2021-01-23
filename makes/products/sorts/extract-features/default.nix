{ path
, sortsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/products/sorts/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSortsRuntime = config.setupSortsRuntime;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path sortsPkgs;
    envUtilsBashLibGit = import (path "/makes/utils/use-git-repo") path sortsPkgs;
    envUtilsMeltsLibCommon = import (path "/makes/lib/melts") attrs.copy;
  };
  location = "/bin/sorts-extract-features";
  name = "sorts-extract-features";
  template = path "/makes/products/sorts/extract-features/entrypoint.sh";
}

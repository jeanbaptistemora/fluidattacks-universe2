{ sortsPkgs
, ...
} @ attrs:
let
  config = import ../../../makes/sorts/config attrs.copy;
  makeEntrypoint = import ../../../makes/utils/make-entrypoint sortsPkgs;
in
makeEntrypoint {
  arguments = {
    envSetupSortsRuntime = config.setupSortsRuntime;
    envUtilsBashLibAws = import ../../../makes/utils/bash-lib/aws sortsPkgs;
    envUtilsBashLibGit = import ../../../makes/utils/bash-lib/use-git-repo sortsPkgs;
    envUtilsMeltsLibCommon = import ../../../makes/utils/melts-lib attrs.copy;
  };
  location = "/bin/sorts-extract-features";
  name = "sorts-extract-features";
  template = ../../../makes/sorts/extract-features/entrypoint.sh;
}

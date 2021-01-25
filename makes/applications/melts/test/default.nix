{ meltsPkgs
, path
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path meltsPkgs;
in
makeEntrypoint {
  arguments = {
    envUtilsBashLibUseGitRepo = import (path "/makes/utils/use-git-repo") path meltsPkgs;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path meltsPkgs;
    envSetupMeltsRuntime = import (path "/makes/packages/melts/config-runtime") attrs.copy;
    envSetupMeltsDevelopment = import (path "/makes/packages/melts/config-development") attrs.copy;
  };
  name = "melts-test";
  template = path "/makes/applications/melts/test/entrypoint.sh";
}

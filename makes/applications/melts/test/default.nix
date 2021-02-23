{ meltsPkgs
, packages
, path
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path meltsPkgs;
in
makeEntrypoint {
  arguments = {
    envUtilsBashLibUseGitRepo = import (path "/makes/utils/use-git-repo") path meltsPkgs;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path meltsPkgs;
    envSetupMeltsRuntime = packages.melts.config-runtime;
    envSetupMeltsDevelopment = packages.melts.config-development;
  };
  name = "melts-test";
  template = path "/makes/applications/melts/test/entrypoint.sh";
}

{ meltsPkgs
, path
, ...
} @ attrs:
let
  config = import (path "/makes/products/melts/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path meltsPkgs;
in
makeEntrypoint {
  arguments = {
    envUtilsBashLibUseGitRepo = import (path "/makes/utils/use-git-repo") path meltsPkgs;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path meltsPkgs;
    envSetupMeltsRuntime = config.setupMeltsRuntime;
    envSetupMeltsDevelopment = config.setupMeltsDevelopment;
  };
  location = "/bin/melts-test";
  name = "melts-test";
  template = path "/makes/products/melts/test/entrypoint.sh";
}

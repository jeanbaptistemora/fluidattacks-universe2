{ meltsPkgs
, ...
} @ attrs:
let
  config = import ../../../makes/melts/config attrs.copy;
  makeEntrypoint = import ../../../makes/utils/make-entrypoint meltsPkgs;
in
makeEntrypoint {
  arguments = {
    envUtilsBashLibUseGitRepo = import ../../../makes/utils/bash-lib/use-git-repo meltsPkgs;
    envUtilsBashLibAws = import ../../../makes/utils/bash-lib/aws meltsPkgs;
    envSetupMeltsRuntime = config.setupMeltsRuntime;
    envSetupMeltsDevelopment = config.setupMeltsDevelopment;
  };
  location = "/bin/melts-test";
  name = "melts-test";
  template = ../../../makes/melts/test/entrypoint.sh;
}

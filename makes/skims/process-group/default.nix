{ outputs
, path
, skimsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/skims/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envJq = "${skimsPkgs.jq}/bin/jq";
    envUtilsBashLibUseGitRepo = import (path "/makes/utils/use-git-repo") path skimsPkgs;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path skimsPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path skimsPkgs;
    envSetupSkimsRuntime = config.setupSkimsRuntime;
    envMelts = outputs.apps.melts.program;
    envSkims = outputs.apps.skims.program;
    envTee = "${skimsPkgs.coreutils}/bin/tee";
    envYq = "${skimsPkgs.yq}/bin/yq";
  };
  location = "/bin/skims-process-group";
  name = "skims-process-group";
  template = path "/makes/skims/process-group/entrypoint.sh";
}

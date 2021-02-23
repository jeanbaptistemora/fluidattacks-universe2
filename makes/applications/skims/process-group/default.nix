{ applications
, packages
, path
, skimsPkgs
, ...
}:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envJq = "${skimsPkgs.jq}/bin/jq";
    envUtilsBashLibAws = import (path "/makes/utils/aws") path skimsPkgs;
    envUtilsBashLibGit = import (path "/makes/utils/git") path skimsPkgs;
    envUtilsBashLibSops = import (path "/makes/utils/sops") path skimsPkgs;
    envSetupSkimsRuntime = packages.skims.config-runtime;
    envMelts = applications.melts;
    envSkims = applications.skims;
    envTee = "${skimsPkgs.coreutils}/bin/tee";
    envYq = "${skimsPkgs.yq}/bin/yq";
  };
  name = "skims-process-group";
  template = path "/makes/applications/skims/process-group/entrypoint.sh";
}

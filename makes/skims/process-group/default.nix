attrs @ {
  outputs,
  skimsBenchmarkOwaspRepo,
  skimsPkgs,
  ...
}:

let
  config = import ../../../makes/skims/config attrs.copy;
  makeEntrypoint = import ../../../makes/utils/make-entrypoint skimsPkgs;
in
  makeEntrypoint {
    arguments = {
      envJq = "${skimsPkgs.jq}/bin/jq";
      envUtilsBashLibUseGitRepo = import ../../../makes/utils/bash-lib/use-git-repo skimsPkgs;
      envUtilsBashLibAws = import ../../../makes/utils/bash-lib/aws skimsPkgs;
      envUtilsBashLibSops = import ../../../makes/utils/bash-lib/sops skimsPkgs;
      envSetupSkimsRuntime = config.setupSkimsRuntime;
      envMelts = outputs.apps.melts.program;
      envSkims = outputs.apps.skims.program;
      envTee = "${skimsPkgs.coreutils}/bin/tee";
      envYq = "${skimsPkgs.yq}/bin/yq";
    };
    location = "/bin/skims-process-group";
    name = "skims-process-group";
    template = ../../../makes/skims/process-group/entrypoint.sh;
  }

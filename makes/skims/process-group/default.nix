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
      envUtilsBashLibAws = import ../../../makes/utils/bash-lib/aws skimsPkgs;
      envUtilsBashLibSops = import ../../../makes/utils/bash-lib/sops skimsPkgs;
      envSetupSkimsRuntime = config.setupSkimsRuntime;
      envSkims = outputs.apps.skims.program;
    };
    location = "/bin/skims-process-group";
    name = "skims-process-group";
    template = ../../../makes/skims/process-group/entrypoint.sh;
  }

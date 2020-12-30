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
      envBenchmarkRepo = skimsBenchmarkOwaspRepo;
      envSetupSkimsRuntime = config.setupSkimsRuntime;
      envSetupSkimsDevelopment = config.setupSkimsDevelopment;
      envUtilsBashLibAws = import ../../../makes/utils/bash-lib/aws skimsPkgs;
    };
    location = "/bin/skims-test";
    name = "skims-test";
    template = ../../../makes/skims/test/entrypoint.sh;
  }

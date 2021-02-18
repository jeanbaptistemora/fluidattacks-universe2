{ packages
, path
, skimsBenchmarkOwaspRepo
, skimsPkgs
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envBenchmarkRepo = skimsBenchmarkOwaspRepo;
    envSetupSkimsDevelopment = packages.skims.config-development;
    envSetupSkimsRuntime = packages.skims.config-runtime;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path skimsPkgs;
  };
  name = "skims-test";
  template = path "/makes/applications/skims/test/entrypoint.sh";
}

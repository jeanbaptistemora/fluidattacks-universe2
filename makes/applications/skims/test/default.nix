{ path
, skimsBenchmarkOwaspRepo
, skimsPkgs
, ...
} @ attrs:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envBenchmarkRepo = skimsBenchmarkOwaspRepo;
    envSetupSkimsDevelopment = import (path "/makes/packages/skims/config-development") attrs.copy;
    envSetupSkimsRuntime = import (path "/makes/packages/skims/config-runtime") attrs.copy;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path skimsPkgs;
  };
  name = "skims-test";
  template = path "/makes/applications/skims/test/entrypoint.sh";
}

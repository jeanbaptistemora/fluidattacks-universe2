{ path
, skimsBenchmarkOwaspRepo
, skimsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/products/skims/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envBenchmarkRepo = skimsBenchmarkOwaspRepo;
    envSetupSkimsRuntime = config.setupSkimsRuntime;
    envSetupSkimsDevelopment = config.setupSkimsDevelopment;
    envUtilsBashLibAws = import (path "/makes/utils/aws") path skimsPkgs;
  };
  location = "/bin/skims-test";
  name = "skims-test";
  template = path "/makes/products/skims/test/entrypoint.sh";
}

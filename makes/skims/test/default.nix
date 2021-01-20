{ path
, skimsBenchmarkOwaspRepo
, skimsPkgs
, ...
} @ attrs:
let
  config = import (path "/makes/skims/config") attrs.copy;
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") skimsPkgs;
in
makeEntrypoint {
  arguments = {
    envBenchmarkRepo = skimsBenchmarkOwaspRepo;
    envSetupSkimsRuntime = config.setupSkimsRuntime;
    envSetupSkimsDevelopment = config.setupSkimsDevelopment;
    envUtilsBashLibAws = import (path "/makes/utils/bash-lib/aws") skimsPkgs;
  };
  location = "/bin/skims-test";
  name = "skims-test";
  template = (path "/makes/skims/test/entrypoint.sh");
}

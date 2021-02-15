{ applications
, integratesPkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
let
  makeSearchPaths = import (path "/makes/utils/make-search-paths-deprecated") path integratesPkgs;
in
makeEntrypoint integratesPkgs {
  arguments = {
    envAsgi = "${integratesPkgs.python37Packages.gunicorn}/bin/gunicorn";
    envCertsDevelopment = packages."integrates/back/certs/development";
    envDone = applications."makes/done";
    envIntegrates = path "/integrates";
    envKillPidListeningOnPort = import (path "/makes/utils/kill-pid-listening-on-port") path integratesPkgs;
    envSearchPaths = makeSearchPaths [
      # Libmagic
      integratesPkgs.file
      # Libstdc++
      integratesPkgs.gcc.cc
      # The binary for pypi://GitPython
      integratesPkgs.git
      # The binary to zip the data report
      integratesPkgs.p7zip
    ];
    envTools = packages."integrates/back/tools";
    envPypiRuntime = packages."integrates/back/pypi/runtime";
    envSecretsDev = path "/integrates/secrets-development.yaml";
    envSecretsProd = path "/integrates/secrets-production.yaml";
    envUtilsAws = import (path "/makes/utils/aws") path integratesPkgs;
    envUtilsSops = import (path "/makes/utils/sops") path integratesPkgs;
    envWait = applications."makes/wait";
  };
  name = "integrates-back";
  searchPaths = {
    envSources = [
      packages."integrates/secrets/list"
    ];
  };
  template = path "/makes/applications/integrates/back/entrypoint.sh";
}

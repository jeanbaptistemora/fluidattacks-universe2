{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  arguments = {
    envCertsDevelopment = packages."integrates/back/certs/development";
    envIntegrates = path "/integrates";
    envKillPidListeningOnPort = import (path "/makes/utils/kill-pid-listening-on-port") path integratesPkgs;
    envSecretsDev = path "/integrates/secrets-development.yaml";
    envSecretsProd = path "/integrates/secrets-production.yaml";
  };
  name = "integrates-back";
  searchPaths = {
    envLibraries = [
      # Libmagic
      integratesPkgs.file
    ];
    envPaths = [
      # The binary for pypi://GitPython
      integratesPkgs.git
      # The binary for the ASGI
      integratesPkgs.python37Packages.gunicorn
      # The binary to zip the data report
      integratesPkgs.p7zip
      packages."makes/done"
      packages."makes/wait"
    ];
    envSources = [
      (import (path "/makes/utils/make-search-paths-deprecated") path integratesPkgs [
        # Libstdc++
        integratesPkgs.gcc.cc
      ])
      packages."integrates/back/pypi/runtime"
      packages."integrates/back/tools"
      packages."integrates/secrets/list"
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/applications/integrates/back/entrypoint.sh";
}

{ integratesPkgs
, makeEntrypoint
, packages
, path
, ...
} @ _:
makeEntrypoint integratesPkgs {
  arguments = {
    envCertsDevelopment = packages."integrates/back/certs/development";
    envIntegratesEnv = packages."integrates/back/env";
    envKillPidListeningOnPort = import (path "/makes/utils/kill-pid-listening-on-port") path integratesPkgs;
  };
  name = "integrates-back";
  searchPaths = {
    envPaths = [
      packages."makes/done"
      packages."makes/wait"
    ];
  };
  template = path "/makes/applications/integrates/back/entrypoint.sh";
}

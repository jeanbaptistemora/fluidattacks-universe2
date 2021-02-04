{ integratesPkgs
, outputs
, path
, ...
} @ _:
let
  makeEntrypoint = import (path "/makes/utils/make-entrypoint") path integratesPkgs;
  makeSearchPaths = import (path "/makes/utils/make-search-paths") path integratesPkgs;
in
makeEntrypoint {
  arguments = {
    envAsgi = "${integratesPkgs.python37Packages.gunicorn}/bin/gunicorn";
    envCertsDevelopment = outputs.packages."integrates/back/certs/development";
    envKillPidListeningOnPort = import (path "/makes/utils/kill-pid-listening-on-port") path integratesPkgs;
    envSearchPaths = makeSearchPaths [
      # Libmagic
      integratesPkgs.file
      # Libstdc++
      integratesPkgs.gcc.cc
      # The binary for pypi://GitPython
      integratesPkgs.git
    ];
    envTools = outputs.packages."integrates/back/tools";
    envPypiRuntime = outputs.packages."integrates/back/pypi/runtime";
    envSecretsDev = path "/integrates/secrets-development.yaml";
    envSecretsProd = path "/integrates/secrets-production.yaml";
    envUtilsAws = import (path "/makes/utils/aws") path integratesPkgs;
    envUtilsSops = import (path "/makes/utils/sops") path integratesPkgs;
    envWait = outputs.apps."makes/wait".program;
  };
  name = "integrates-back";
  template = path "/makes/packages/integrates/back/bin/entrypoint.sh";
}

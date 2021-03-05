{ integratesPkgs
, makeTemplate
, packages
, path
, ...
}:
makeTemplate {
  arguments = {
    envIntegrates = path "/integrates";
    envSecretsDev = path "/integrates/secrets-development.yaml";
    envSecretsProd = path "/integrates/secrets-production.yaml";
  };
  name = "integrates-back-env";
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
    ];
    envSources = [
      (import (path "/makes/utils/make-search-paths-deprecated") path integratesPkgs [
        # Libstdc++
        integratesPkgs.gcc.cc
      ])
      packages.integrates.back.pypi.runtime
      packages.integrates.back.tools
      packages.integrates.secrets.list
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/packages/integrates/back/env/template.sh";
}

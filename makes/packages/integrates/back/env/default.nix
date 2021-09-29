{ nixpkgs
, makes
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
      nixpkgs.file
      # Required by matplotlib
      nixpkgs.gcc.cc.lib
    ];
    envPaths = [
      # The binary for pypi://GitPython
      nixpkgs.git
      # The binary for the ASGI
      nixpkgs.python37Packages.gunicorn
      # The binary to zip the data report
      nixpkgs.p7zip
    ];
    envSources = [
      packages.skims.config-sdk
      packages.integrates.back.pypi.runtime
      packages.integrates.back.tools
      packages.integrates.secrets.list
      makes.libGit
    ];
    envUtils = [
      "/makes/utils/aws"
      "/makes/utils/sops"
    ];
  };
  template = path "/makes/packages/integrates/back/env/template.sh";
}

{ nixpkgs
, lintPython
, makeDerivation
, packages
, path
, ...
} @ _:
makeDerivation {
  arguments = {
    envIntegrates = path "/integrates";
    envIntegratesImportsConfig = path "/integrates/back/setup.imports.cfg";
    envProspectorSettings = path "/makes/utils/lint-python/settings-prospector.yaml";
  };
  builder = path "/makes/packages/integrates/back/lint/builder.sh";
  name = "integrates-back-lint";
  searchPaths = {
    envPaths = [
      nixpkgs.python37
    ];
    envSources = [
      lintPython
      packages.integrates.back.pypi.runtime
      packages.skims.config-sdk
    ];
  };
}

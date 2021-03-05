{ nixpkgs
, lintPython
, makeDerivation
, packages
, path
, ...
} @ _:
makeDerivation {
  arguments = {
    envIntegratesBackModules = path "/integrates/back/packages/modules";
    envIntegratesImportsConfig = path "/integrates/back/setup.imports.cfg";
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
    ];
  };
}

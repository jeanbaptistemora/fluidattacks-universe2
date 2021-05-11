{ nixpkgs
, lintPython
, makeDerivation
, packages
, path
, ...
} @ _:
makeDerivation {
  arguments = {
    envIntegratesBack = path "/integrates/back";
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

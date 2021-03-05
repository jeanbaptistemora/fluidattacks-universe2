{ integratesPkgs
, lintPython
, makeDerivation
, packages
, path
, ...
} @ _:
makeDerivation integratesPkgs {
  arguments = {
    envIntegratesBackModules = path "/integrates/back/packages/modules";
    envIntegratesImportsConfig = path "/integrates/back/setup.imports.cfg";
  };
  builder = path "/makes/packages/integrates/back/lint/builder.sh";
  name = "integrates-back-lint";
  searchPaths = {
    envPaths = [
      integratesPkgs.python37
    ];
    envSources = [
      (lintPython integratesPkgs)
      packages.integrates.back.pypi.runtime
    ];
  };
}

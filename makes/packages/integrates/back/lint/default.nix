{ integratesPkgs
, lintPython
, makeDerivation
, packages
, path
, ...
} @ _:
makeDerivation integratesPkgs {
  arguments = {
    envIntegratesSrc = path "/integrates";
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

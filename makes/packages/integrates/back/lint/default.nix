{ integratesPkgs
, makeUtils
, packages
, path
, ...
} @ _:
makeUtils.makeDerivation integratesPkgs {
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
      (makeUtils.lintPython integratesPkgs)
      packages.integrates.back.pypi.runtime
    ];
  };
}

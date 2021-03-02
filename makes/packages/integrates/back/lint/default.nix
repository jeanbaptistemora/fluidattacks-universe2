{ integratesPkgs
, makeUtils
, packages
, path
, ...
} @ _:
makeUtils.makeDerivation integratesPkgs {
  arguments = {
    envIntegratesBackModules = path "/integrates/back/packages/modules";
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

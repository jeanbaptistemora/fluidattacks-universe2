{ lintPython
, makeDerivation
, packages
, path
, integratesPkgs
, ...
} @ _:
makeDerivation integratesPkgs {
  builder = path "/makes/packages/integrates/web/e2e/lint/builder.sh";
  envSrc = path "/integrates/test_e2e/src";
  name = "integrates-web-e2e-lint";
  searchPaths = {
    envPython38Paths = [
      packages.integrates.web.e2e.pypi
    ];
    envSources = [
      (lintPython integratesPkgs)
    ];
  };
}

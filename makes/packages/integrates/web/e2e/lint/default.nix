{ lintPython
, makeDerivation
, packages
, path
, integratesPkgs
, ...
} @ _:
makeDerivation integratesPkgs {
  arguments = {
    envSrc = path "/integrates/test_e2e/src";
  };
  builder = path "/makes/packages/integrates/web/e2e/lint/builder.sh";
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

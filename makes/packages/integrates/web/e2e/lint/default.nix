{ lintPython
, makeDerivation
, packages
, path
, ...
}:
makeDerivation {
  arguments = {
    envSrc = path "/integrates/back/tests/e2e/src";
  };
  builder = path "/makes/packages/integrates/web/e2e/lint/builder.sh";
  name = "integrates-web-e2e-lint";
  searchPaths = {
    envPython38Paths = [
      packages.integrates.web.e2e.pypi
    ];
    envSources = [
      lintPython
    ];
  };
}

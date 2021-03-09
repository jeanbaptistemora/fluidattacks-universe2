{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-lint-code-etl";
  arguments = {
    envSrc = path "/observes/code_etl";
    envTestDir = "tests";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.tester
      packages.observes.env.development.code-etl
    ];
  };
  builder = path "/makes/packages/observes/test/code-etl/builder.sh";
}

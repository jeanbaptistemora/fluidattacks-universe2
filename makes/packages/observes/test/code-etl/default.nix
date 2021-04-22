{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-test-code-etl";
  arguments = {
    envSrc = path "/observes/code_etl";
    envTestDir = "tests";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.tester
      packages.observes.env.code-etl.development
    ];
  };
  builder = path "/makes/packages/observes/generic/tester/test_builder.sh";
}

{ makeDerivation
, path
, packages
, ...
}:
makeDerivation {
  name = "observes-test-postgres-client";
  arguments = {
    envSrc = path "/observes/common/postgres_client";
    envTestDir = "tests";
  };
  searchPaths = {
    envSources = [
      packages.observes.generic.tester
      packages.observes.env.postgres-client.development
    ];
  };
  builder = path "/makes/packages/observes/generic/tester/test_builder.sh";
}

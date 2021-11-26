{ makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  name = "observes-common-postgres-client-test";
  env = {
    envSrc = projectPath "/observes/common/postgres_client";
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."/observes/common/postgres-client/env/development"
    ];
  };
  builder = projectPath "/makes/foss/units/observes/common/tester/test_builder.sh";
}

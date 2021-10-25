{ makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  builder = projectPath "/makes/foss/units/observes/common/tester/test_builder.sh";
  env = {
    envSrc = projectPath "/observes/code_etl";
    envTestDir = "tests";
  };
  name = "observes-test-code-etl";
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."/observes/env/code-etl/development"
    ];
  };
}

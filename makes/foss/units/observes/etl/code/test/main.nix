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
  name = "observes-etl-code-test";
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."/observes/etl/code/env/development"
    ];
  };
}

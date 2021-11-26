{ makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  name = "observes-common-singer-io-test";
  env = {
    envSrc = projectPath "/observes/common/singer_io";
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."/observes/common/singer-io/env/development"
    ];
  };
  builder = projectPath "/makes/foss/units/observes/common/tester/test_builder.sh";
}

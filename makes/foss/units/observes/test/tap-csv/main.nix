{ makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  name = "observes-test-tap-csv";
  env = {
    envSrc = projectPath "/observes/singer/tap_csv";
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."/observes/singer/tap-csv/env/development"
    ];
  };
  builder = projectPath "/makes/foss/units/observes/common/tester/test_builder.sh";
}

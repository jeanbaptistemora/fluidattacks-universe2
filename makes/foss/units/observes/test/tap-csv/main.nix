{ inputs
, makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  name = "observes-test-tap-csv";
  env = {
    envSrc = projectPath inputs.observesIndex.tap.csv.root;
    envTestDir = baseNameOf inputs.observesIndex.tap.csv.tests;
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.csv.env.dev}"
    ];
  };
  builder = projectPath "/makes/foss/units/observes/common/tester/test_builder.sh";
}

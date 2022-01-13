{ inputs
, makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  name = "observes-test-tap-mixpanel";
  env = {
    envSrc = projectPath inputs.observesIndex.tap.mixpanel.root;
    envTestDir = baseNameOf inputs.observesIndex.tap.mixpanel.tests;
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.mixpanel.env.dev}"
    ];
  };
  builder = projectPath "/makes/foss/units/observes/common/tester/test_builder.sh";
}

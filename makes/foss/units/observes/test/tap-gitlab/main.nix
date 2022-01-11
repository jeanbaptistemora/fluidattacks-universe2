{ inputs
, makeDerivation
, outputs
, projectPath
, ...
}:
makeDerivation {
  name = "observes-test-tap-gitlab";
  env = {
    envSrc = projectPath inputs.observesIndex.tap.gitlab.root;
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.gitlab.env.dev}"
    ];
  };
  builder = projectPath "/makes/foss/units/observes/common/tester/test_builder.sh";
}

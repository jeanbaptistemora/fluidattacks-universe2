{
  inputs,
  makeDerivation,
  outputs,
  projectPath,
  ...
}:
makeDerivation {
  name = "observes-singer-tap-announcekit-test";
  env = {
    envSrc = projectPath inputs.observesIndex.tap.announcekit.root;
    envTestDir = baseNameOf inputs.observesIndex.tap.announcekit.tests;
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.announcekit.env.dev}"
    ];
  };
  builder = projectPath "/observes/common/tester/test_builder.sh";
}

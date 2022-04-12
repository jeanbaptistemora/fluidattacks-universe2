{
  inputs,
  makeDerivation,
  outputs,
  projectPath,
  ...
}:
makeDerivation {
  name = "observes-singer-tap-gitlab-test";
  env = {
    envSrc = projectPath inputs.observesIndex.tap.gitlab.root;
    envTestDir = baseNameOf inputs.observesIndex.tap.gitlab.tests;
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.gitlab.env.dev}"
    ];
  };
  builder = projectPath "/observes/common/tester/test_builder.sh";
}

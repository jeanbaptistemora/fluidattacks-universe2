{
  inputs,
  makeDerivation,
  outputs,
  projectPath,
  ...
}:
makeDerivation {
  name = "observes-singer-tap-mailchimp-test";
  env = {
    envSrc = projectPath inputs.observesIndex.tap.mailchimp.root;
    envTestDir = "tests";
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.mailchimp.env.dev}"
    ];
  };
  builder = projectPath "/observes/common/tester/test_builder.sh";
}

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
    envTestDir = baseNameOf inputs.observesIndex.tap.mailchimp.tests;
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.mailchimp.env.dev}"
    ];
  };
  builder = projectPath "/makes/foss/units/observes/common/tester/test_builder.sh";
}

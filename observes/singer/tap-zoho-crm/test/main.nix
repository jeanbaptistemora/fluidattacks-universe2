{
  inputs,
  makeDerivation,
  outputs,
  projectPath,
  ...
}:
makeDerivation {
  name = "observes-singer-zoho-crm-test";
  env = {
    envSrc = projectPath inputs.observesIndex.tap.zoho_crm.root;
    envTestDir = baseNameOf inputs.observesIndex.tap.zoho_crm.tests;
  };
  searchPaths = {
    source = [
      outputs."/observes/common/tester"
      outputs."${inputs.observesIndex.tap.zoho_crm.env.dev}"
    ];
  };
  builder = projectPath "/observes/common/tester/test_builder.sh";
}
